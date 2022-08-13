# Программа клиента, запрашивающего текущее время
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
from base import *


def cr_presen(name='Test'):
    result = {ACTION: PRESENCE, TIME: time.time(), USER: {ACC_NAME: name}}
    return result


def proc_ans(mess):
    if RESPONSE in mess:
        if mess[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {mess[ERROR]}'
    raise ValueError


def main():
    try:
        serv_addr = sys.argv[1]
        serv_port = int(sys.argv[2])
        if serv_port > 65535 or serv_port < 1024:
            raise ValueError
    except IndexError:
        serv_addr = IP
        serv_port = PORT
    except ValueError:
        print('1024 < Port < 65535')
        sys.exit(1)

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((serv_addr, serv_port))
    to_byte(s, cr_presen())
    try:
        print(proc_ans(from_byte(s)))
    except:
        print("not connect")

    # tm = s.recv(1024)  # Принять не более 1024 байтов данных
    # s.close()


if __name__ == '__main__':
    main()
