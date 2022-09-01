# -*- coding: utf-8 -*-
# Программа сервера времени
from base import *
import log.server_log_config
from dec import log

LOG = logging.getLogger('server')


@log
def proc_client_message(mess, mess_list, client):
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
    if ACTION in mess and mess[ACTION] == PRESENCE and TIME in mess \
            and USER in mess and mess[USER][ACCOUNT_NAME] == 'Test':
        to_byte(client, {RESPONSE: 200})
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in mess and mess[ACTION] == MESSAGE and \
            TIME in mess and MESSAGE_TEXT in mess:
        mess_list.append((mess[ACCOUNT_NAME], mess[MESSAGE_TEXT]))
        return
    # Иначе отдаём Bad request
    else:
        to_byte(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


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

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            LOG.info(f'Connect to client {client_address}')
            clients.append(client)

        # mass listen and write client
        list_data_lst = []
        send_data_lst = []
        err_lst = []

        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                list_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if list_data_lst:
            for client_with_message in list_data_lst:
                try:
                    proc_client_message(from_byte(client_with_message),
                                        messages, client_with_message)
                except:
                    LOG.info(f'Client {client_with_message.getpeername()} to close')
                    clients.remove(client_with_message)
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    to_byte(waiting_client, message)
                except:
                    LOG.info(f'Client {waiting_client.getpeername()} to close')
                    clients.remove(waiting_client)





if __name__ == '__main__':
    main()
