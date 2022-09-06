"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
(Внимание! Аргументом сабпроцесcа должен быть список, а не строка!!!
Для уменьшения времени работы скрипта при проверке нескольких ip-адресов, решение необходимо выполнить с помощью потоков)
"""
import os
import platform
import subprocess
import time
from ipaddress import ip_address
from threading import Thread

result = {"Reachable": '', "Unreachable": ''}
addrs = ['192.168.1.0', '192.168.1.255', '192.168.1.0', 'google.com', 'a', '123.45', 'yandex.ru',
         '192.168.1.0', '192.168.1.255', '192.168.1.0', 'google.com', 'a', '123.45', 'yandex.ru',
         '192.168.1.0', '192.168.1.255', '192.168.1.0', 'google.com', 'a', '123.45', 'yandex.ru',
         '192.168.1.0', '192.168.1.255', '192.168.1.0', 'google.com', 'a', '123.45', 'yandex.ru']

# DNULL = open(os.devnull, 'w') - не понял зачем ?


def check_is_ipaddress(val):
    try:
        ip = ip_address(val)
    except ValueError:
        raise Exception("ip_address() return except 'ValueError' - not correct ip address,")
    return ip


def host_ping(host_list, get_list=False):


    def hp(host):
        try:
            ipv4 = check_is_ipaddress(host)
        except Exception as e:
            # print(f'{host} - {e} how domain name')
            ipv4 = str(host)

        if platform.system().lower() == 'windows':
            param = '-n'
        else:
            param = '-c'

        responce = subprocess.Popen(["ping", param, '1', '-w', '1', str(ipv4)], stdout=subprocess.PIPE)

        if responce.wait() == 0:
            result["Reachable"] += f'{ipv4}\n'
            res_string = f'{ipv4} - Узел доступен'
        else:
            result["Unreachable"] += f'{ipv4}\n'
            res_string = f'{ipv4} - Узел недоступен'

        if not get_list:
            print(res_string)

    THR = host_list

    for i in range(len(THR)):
        THR[i] = Thread(target=hp, args=(host_list[i],))
        THR[i].start()

    for i in range(len(THR)):
        THR[i].join()

    if get_list:
        return result


if __name__ == '__main__':

    # start = time.time()
    # THR = addrs
    #
    # for i in range(len(THR)):
    #     THR[i] = Thread(target=host_ping, args=(addrs[i],))
    #     THR[i].start()
    #
    # for i in range(len(THR)):
    #     THR[i].join()
    #
    # end = time.time()
    # print(f'total time: {int(end - start)}')
    host_ping(addrs)
