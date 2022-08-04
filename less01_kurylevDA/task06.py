# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
# программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

import chardet

neededFile = open("test_file.txt", 'rb')
rawdata = neededFile.read()
enc = chardet.detect(rawdata)

print(rawdata.decode(enc['encoding']))

neededFile.close()