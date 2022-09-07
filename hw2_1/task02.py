"""
2. Написать функцию host_range_ping() (возможности которой основаны на функции из примера 1)
для перебора ip-адресов из заданного диапазона. Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""
from pprint import pprint

from task01 import host_ping


def host_range_ping():

    addr = input("input address: ")
    while True:
        count = int(input("input number last octet: "))
        if count > 256:
            print("max number octet = 256")
            continue
        else:
            break

    addr_list = []
    a = addr.split('.')
    for i in range(count):
        addr_list.append(a[0] + '.' + a[1] + '.' + a[2] + '.' + str(int(a[3]) + i))

    result = host_ping(addr_list, get_list=True)
    return result

if __name__ == '__main__':
    host_range_ping()