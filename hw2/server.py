import socket
import sys
import argparse
import json
import logging
import threading

import select
import time
import logs.config_server_log
from errors import IncorrectDataRecivedError
from common.variables import *
from common.utils import *
from decos import log

# Инициализация логирования сервера.
from descripts import Port
from metaclasses import SreverMaker
from server_db_decl import ServerDB

logger = logging.getLogger('server_dist')


# Парсер аргументов командной строки.
@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


# Основной класс сервера
class Server(threading.Thread, metaclass=SreverMaker):
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        # Параметры подключения
        self.addr = listen_address
        self.port = listen_port

        # База данных сервера
        self.database = database

        # Список подключённых клиентов.
        self.clients = []

        # Список сообщений на отправку.
        self.messages = []

        # Словарь содержащий сопоставленные имена и соответствующие им сокеты.
        self.names = dict()

        # Конструктор предка
        super().__init__()

    def init_socket(self):
        logger.info(
            f'Запущен сервер, порт для подключений: {self.port}, '
            f'адрес с которого принимаются подключения: {self.addr}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')
        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # setsockopt устанавливает значение value данной опции optname сокета
        # SOL_SOCKET: Общий параметр сокета, SO_REUSEADDR Разрешить повторное использование локального адреса и порта
        transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        # Начинаем слушать сокет.
        self.sock = transport
        self.sock.listen()

    def run(self):
        # Инициализация Сокета
        self.init_socket()

        # Основной цикл программы сервера
        while True:
            # Ждём подключения, если таймаут вышел, ловим исключение.
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                logger.info(f'Установлено соедение с ПК {client_address}')
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            # Проверяем на наличие ждущих клиентов
            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            # принимаем сообщения и если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(get_message(client_with_message), client_with_message)
                    except:
                        logger.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                        self.clients.remove(client_with_message)

            # Если есть сообщения, обрабатываем каждое.
            for message in self.messages:
                try:
                    self.process_message(message, send_data_lst)
                except Exception as e:
                    logger.info(f'Связь с клиентом с именем '
                                f'{message[DESTINATION]} была потеряна, '
                                f' ошибка {e}')
                    self.clients.remove(self.names[message[DESTINATION]])
                    del self.names[message[DESTINATION]]
            self.messages.clear()

    # Функция адресной отправки сообщения определённому клиенту.
    # Принимает словарь сообщение, список зарегистрированных
    # пользователей и слушающие сокеты. Ничего не возвращает.
    def process_message(self, message, listen_socks):
        if message[DESTINATION] in self.names and \
                self.names[message[DESTINATION]] in listen_socks:
            send_message(self.names[message[DESTINATION]], message)
            logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                        f'от пользователя {message[SENDER]}.')
        elif message[DESTINATION] in self.names \
                and self.names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError
        else:
            logger.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован '
                f'на сервере, отправка сообщения невозможна.')

    # Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
    # проверяет корректность, отправляет словарь-ответ в случае необходимости.
    def process_client_message(self, message, client):
        logger.debug(f'Разбор сообщения от клиента : {message}')
        # Если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in message and message[ACTION] == PRESENCE \
                and TIME in message and USER in message:
            # Если такой пользователь ещё не зарегистрирован, регистрируем,
            # иначе отправляем ответ и завершаем соединение.
            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                client_ip, client_port = client.getpeername()
                self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port)
                send_message(client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято.'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
        # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
        elif ACTION in message \
                and message[ACTION] == MESSAGE \
                and DESTINATION in message \
                and TIME in message \
                and SENDER in message \
                and MESSAGE_TEXT in message:
            self.messages.append(message)
            return
        # Если клиент выходит
        elif ACTION in message \
                and message[ACTION] == EXIT \
                and ACCOUNT_NAME in message:
            self.database.user_logout(message[ACCOUNT_NAME])
            self.clients.remove(self.names[ACCOUNT_NAME])
            self.names[ACCOUNT_NAME].close()
            del self.names[ACCOUNT_NAME]
            return
        # Иначе отдаём Bad request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            send_message(client, response)
            return

def print_help():
    print('Поддерживаемые комманды:')
    print('users - список известных пользователей')
    print('connected - список подключённых пользователей')
    print('loghist - история входов пользователя')
    print('exit - завершение работы сервера.')
    print('help - вывод справки по поддерживаемым командам')

def main():
    # Загрузка параметров командной строки, если нет параметров,
    # то задаём значения по умолчанию.
    listen_address, listen_port = arg_parser()

    # Инициализация базы данных
    database = ServerDB()

    # Создание экземпляра класса - сервера.
    server = Server(listen_address, listen_port, database)
    # запускаем как поток
    server.daemon = True
    server.start()

    # Печатаем справку:
    print_help()

    # Основной цикл сервера:
    while True:
        command = input('Введите команду: ')
        if command == 'help':
            print_help()
        elif command == 'exit':
            break
        elif command == 'users':
            all_users = sorted(database.users_list())
            if all_users:
                for user in all_users:
                    print(f'Пользователь {user[0]}, последний вход: {user[1]}')
            else:
                print('No data')

        elif command == 'connected':
            active_users = sorted(database.active_users_list())
            if active_users:
                for user in active_users:
                    print(f'Пользователь {user[0]}, подключен: {user[1]}:{user[2]}, '
                          f'время установки соединения: {user[3]}')
            else:
                print('No data')
        elif command == 'loghist':
            name = input('Введите имя пользователя для просмотра истории. '
                         'Для вывода всей истории, просто нажмите Enter: ')
            history = sorted(database.login_history(name))
            if history:
                for user in sorted(database.login_history(name)):
                    print(f'Пользователь: {user[0]} время входа: {user[1]}. '
                          f'Вход с: {user[2]}:{user[3]}')
            else:
                print('No data')
        else:
            print('Команда не распознана.')


if __name__ == '__main__':
    main()

