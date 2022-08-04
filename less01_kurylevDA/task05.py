# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
# байтовового в строковый тип на кириллице.


import subprocess
import chardet


hosts = ["yandex.ru", "youtube.com"]

for i in hosts:
    ping = subprocess.Popen(
        ["ping", i],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    out, error = ping.communicate()
    enc = chardet.detect(out)

    print(i)
    print(out.decode(enc['encoding']))