# -*- coding: utf-8 -*-
# Программа клиента, запрашивающего текущее время
import threading

from base import *
import log.client_log_config
from dec import log

LOG = logging.getLogger('client')

@log
def create_exit_message(account_name):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }

@log
def mess_from_server(sock, my_user_name):
    """function working with messages from different client, from server """
    while True:
        try:
            mess = from_byte(sock)
            if ACTION in mess and mess[ACTION] == MESSAGE and SENDER in mess and DESTINATION in mess and MESSAGE_TEXT in mess and mess[DESTINATION] == my_user_name:
                print(f'User {mess[SENDER]}, message: {mess[MESSAGE_TEXT]}')
                LOG.info(f'input message from {mess[SENDER]}, text: {mess[MESSAGE_TEXT]}')
            else:
                LOG.error(f'input not correct message: {mess}')
        except IncorrectDataRecivedError:
            LOG.error('not decode mess')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            LOG.critical(f'Потеряно соединение с сервером.')
            break





@log
def create_mess(sock, account_name='Test'):
    """
    Функция запрашивает кому отправить сообщение и само сообщение,
    и отправляет полученные данные на сервер
    :param sock:
    :param account_name:
    :return:
    """
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    LOG.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        to_byte(sock, message_dict)
        LOG.info(f'Отправлено сообщение для пользователя {to_user}')
    except:
        LOG.critical('Потеряно соединение с сервером.')
        sys.exit(1)

@log
def user_interface(sock, acc_name = 'Test'):
    """input address, and text message, and to message to address"""

    to_user = input("name user for message: ")
    to_mess = input("message: ")
    mess_dict = {
        ACTION: MESSAGE, SENDER: acc_name, DESTINATION: to_user, TIME: time.time(), MESSAGE_TEXT: to_mess
    }
    LOG.debug(f'create dict message: {mess_dict}')
    try:
        to_byte(sock, mess_dict)
        LOG.info(f'message to user')
    except:
        LOG.error('lost connect with server')
        sys.exit(1)

@log
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print(username)
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_mess(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            to_byte(sock, create_exit_message(username))
            print('Завершение соединения.')
            LOG.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')

def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')

@log
def cr_presen(name='Test'):
    """function generate message for presence client"""
    result = {ACTION: PRESENCE, TIME: 1.1, USER: {ACC_NAME: name}}
    LOG.info(f'create dict MESSAGE PRESENCE: {result}')
    return result


@log
def proc_ans(mess):
    """function parses the server's response to the presence message, returns 200 if everything is OK or 400 : error"""
    if RESPONSE in mess:
        if mess[RESPONSE] == 200:
            return '200 : OK'
        elif mess[RESPONSE] == 400:
            raise ServerError(f'400 : {mess[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@log
def arg_parser():
    """Create parser args command line and read options, return 3 options"""
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=IP, nargs='?')
    parser.add_argument('port', default=PORT, type=int, nargs='?')
    parser.add_argument('-n', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.n

    if not 1023 < server_port < 65536:
        LOG.critical(
            f'Attempting to start a client with the wrong port number: {server_port}. '
            f'Valid addresses are 1024 to 65535. The client ends.')
        sys.exit(1)

    return server_address, server_port, client_name


def main():
    server_address, server_port, client_name = arg_parser()

    if not client_name:
        client_name = input("input client name: ")

    LOG.info(f'Client started with parameters: server address: {server_address}, '
             f'port: {server_port}, name user: {client_name}')

    try:
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((server_address, server_port))
        to_byte(transport, cr_presen(client_name))
        answer = proc_ans(from_byte(transport))
        LOG.info(f'Connection to server. Server response: {answer}')
        print(f'Connection to server.')
    except json.JSONDecodeError:
        LOG.error('No decode Json string')
        sys.exit(1)
    except ServerError as error:
        LOG.error(f'Connect to server, return Error: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        LOG.error(f'Required field is missing, server response {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        LOG.critical(
            f'Failed to connect to server {server_address}:{server_port}, '
            f'finish computer rejected the connection request.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # запускаем потоки для работы с клиентами
        # поток для приема сообщений

        receiver = threading.Thread(target=mess_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        # поток для отправки сообщений

        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()


        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
