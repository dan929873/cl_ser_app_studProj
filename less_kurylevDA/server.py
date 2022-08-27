# Программа сервера времени
from base import *
import log.server_log_config
from dec import log

LOG = logging.getLogger('server')

@log
def test_client_mess(mess):
    if ACTION in mess and mess[ACTION] == PRESENCE and TIME in mess \
            and USER in mess and mess[USER][ACC_NAME] == 'Test':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            l_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            l_port = PORT
        if l_port < 1024 or l_port > 65535:
            raise ValueError
    except IndexError:
        LOG.warning('After param -\'p\' need write number port')
        sys.exit(1)
    except ValueError:
        LOG.warning('1024 < port < 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            l_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            l_address = ''

    except IndexError:
        LOG.warning('After param \'a\'- need write number address')
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((l_address, l_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_cient = from_byte(client)
            LOG.info(message_from_cient)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = test_client_mess(message_from_cient)
            to_byte(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            LOG.critical('Received message from client not correct ')
            client.close()


if __name__ == '__main__':
    main()
