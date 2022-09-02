# -*- coding: utf-8 -*-
# Программа сервера времени
from base import *
import log.server_log_config
from dec import log

LOG = logging.getLogger('server')


@log
def proc_client_message(mess, mess_list, client, clients, names):
    """
    Message handler from clients, accepts a dictionary - a message from the client,
    checks the correctness, sends a response dictionary to the client with the result of the reception.
    :param message:
    :param messages_list:
    :param client:
    :return:
    """
    LOG.debug(f'Check message from client : {mess}')
    # Если это сообщение о присутствии, принимаем и отвечаем, если успех
    if ACTION in mess and mess[ACTION] == PRESENCE and TIME in mess and USER in mess:
        if mess[USER][ACCOUNT_NAME] not in names.keys():
            names[mess[USER][ACCOUNT_NAME]] = client
            to_byte(client, {RESPONSE: 200})
        else:
            response = {RESPONSE: 400, ERROR: None}
            response[ERROR] = 'Имя пользователя уже занято.'
            to_byte(client, response)
            clients.remove(client)
            client.close()

    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in mess and mess[ACTION] == MESSAGE and DESTINATION in mess and TIME in mess and SENDER in mess and MESSAGE_TEXT in mess:
        mess_list.append(mess)
        return
    # Если клиент выходит
    elif ACTION in mess and mess[ACTION] == EXIT and ACCOUNT_NAME in mess:
        clients.remove(names[mess[ACCOUNT_NAME]])
        names[mess[ACCOUNT_NAME]].close()
        del names[mess[ACCOUNT_NAME]]
        return
    # Иначе отдаём Bad request
    else:
        response = {RESPONSE: 400, ERROR: None}
        response[ERROR] = 'Запрос некорректен.'
        to_byte(client, response)
        return


@log
def process_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_socks:
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        to_byte(names[message[DESTINATION]], message)
        LOG.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                    f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        LOG.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')

@log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        LOG.critical(
            f'Trying to start the server with an invalid port '
            f'{listen_port}. Valid addresses are 1024 to 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    l_address, l_port = arg_parser()

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((l_address, l_port))
    transport.settimeout(0.5)
    transport.listen(MAX_CONNECTIONS)


    # список клиентов , очередь сообщений
    clients = []
    messages = []
    # Словарь, содержащий имена пользователей и соответствующие им сокеты.
    names = dict()

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            LOG.info(f'Connect to client {client_address}')
            clients.append(client)

        # mass listen and write client
        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    proc_client_message(from_byte(client_with_message),
                                        messages, client_with_message, clients, names)
                except Exception:
                    LOG.info(f'Client {client_with_message.getpeername()} to close')
                    clients.remove(client_with_message)

        # Если есть сообщения, обрабатываем каждое.
        for i in messages:
            try:
                process_message(i, names, send_data_lst)
            except Exception:
                LOG.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
