"""функция запуска нескольких клиентов и сервера. клиент - в режиме "прослушивания" и "написания сообщения" """

import subprocess

PROCESS = []

while True:
    ACTION = input('input type do: q - quit, s - start server and client, x - close all window: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

        try:
            count_client_l = int(input('input count client "listen" type: '))
        except ValueError:
            print ("write number - count, default = 3")
            count_client_l = 3

        for i in range(count_client_l):
            PROCESS.append(subprocess.Popen('python client.py -m listen', creationflags=subprocess.CREATE_NEW_CONSOLE))

        try:
            count_client_s = int(input('input count client "sent" type: '))
        except ValueError:
            print("write number - count, default = 1")
            count_client_s = 1

        for i in range(count_client_s):
            PROCESS.append(subprocess.Popen('python client.py -m sent', creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()

