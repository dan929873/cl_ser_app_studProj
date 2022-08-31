# Программа клиента, запрашивающего текущее время

from base import *
import log.client_log_config
from dec import log

LOG = logging.getLogger('client')


@log
def mess_from_server(mess):
    """function working with messages from different client, from server """
    if ACTION in mess and mess[ACTION] == MESSAGE and \
            SENDER in mess and MESSAGE_TEXT in mess:
        print(f'{mess[SENDER]}: {mess[MESSAGE_TEXT]}')
        LOG.info(f'message input, from clint{mess[SENDER]}: {mess[MESSAGE_TEXT]}')
    else:
        LOG.info(f'message not correct - {mess}')


@log
def create_mess(sock, acc_name='Test'):
    """function make input text for message, and do dar MESSAGE"""
    mess = input('input text message, or !!! for close: ')

    if mess == '!!!':
        sock.close()
        LOG.info('end on command client')
        print('end on command client')
        sys.exit()
    mess_dict = {ACTION: MESSAGE, TIME: time.time(), ACCOUNT_NAME: acc_name, MESSAGE_TEXT: mess}

    LOG.info(f'create dict MESSAGE: {mess_dict}')
    return mess_dict


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
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        LOG.critical(
            f'Attempting to start a client with the wrong port number: {server_port}. '
            f'Valid addresses are 1024 to 65535. The client ends.')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        LOG.critical(f'Invalid operating mode specified {client_mode}, '
                     f'allowed modes: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    server_address, server_port, client_mode = arg_parser()
    LOG.info(f'Client started with parameters: server address: {server_address}, '
             f'port: {server_port}, operating mode: {client_mode}')

    try:
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((server_address, server_port))
        to_byte(transport, cr_presen())
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
        LOG.error(f'required field is missing, server response {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        LOG.critical(
            f'Failed to connect to server {server_address}:{server_port}, '
            f'finish computer rejected the connection request.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('send work')
        else:
            print('listen work')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    to_byte(transport, create_mess(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG.error(f'Connect to server {server_address} failed')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    mess_from_server(from_byte(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG.error(f'Connect to server {server_address} failed')
                    sys.exit(1)


if __name__ == '__main__':
    main()
