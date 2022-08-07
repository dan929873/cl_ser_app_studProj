"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из
файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

    Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
    данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
    «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить
    в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
    os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и
    поместить в него названия столбцов отчета в виде списка:
    «Изготовитель системы»,
    «Название ОС»,
    «Код продукта»,
    «Тип системы».
    Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

    Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение
    данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
    Проверить работу программы через вызов функции write_to_csv().
"""

import chardet
import re
import csv

def find_val(m_str, f_val):
    match = re.search(f_val, m_str)
    start = match.span()[1] + 1
    end = m_str.find('\n', start, start + 100)
    return m_str[start:end].strip()

def get_data():
    os_prod_list, os_name_list, os_code_list, os_type_list, main_data = list(), list(), list(), list(), ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']

    fl = ["info_1.txt", "info_2.txt", "info_3.txt"]
    for iter_file in fl:
        with open(iter_file, 'rb') as of:

            rawdata = of.read()
            enc = chardet.detect(rawdata)
            ml = (rawdata.decode(enc['encoding']))

            os_prod_list.append(find_val(ml, main_data[0]))
            os_name_list.append(find_val(ml, main_data[1]))
            os_code_list.append(find_val(ml, main_data[2]))
            os_type_list.append(find_val(ml, main_data[3]))

    return os_prod_list, os_name_list, os_code_list, os_type_list, main_data




def write_to_csv(name_file):
    os_prod_list, os_name_list, os_code_list, os_type_list, main_data = get_data()

    with open(name_file, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)

        wr.writerow(main_data)
        for i in range(len(os_prod_list)):
            my_list = list()
            my_list.append(os_prod_list[i])
            my_list.append(os_name_list[i])
            my_list.append(os_code_list[i])
            my_list.append(os_type_list[i])
            wr.writerow(my_list)
            print(my_list)



write_to_csv('my_file.csv')

