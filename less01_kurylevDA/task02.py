# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
# последовательность кодов (не используя методы encode и decode) и определить тип,
# содержимое и длину соответствующих переменных.


my_words = [bytearray(b'class'), bytearray(b'function'), bytearray(b'method')]

for i in my_words:
    print(f"type - {type(i)}")
    print(f"word - {bytes(i)}")
    print(f"len  - {len(i)}")


