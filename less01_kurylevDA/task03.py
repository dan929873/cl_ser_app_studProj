# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
# байтовом типе.

my_words = ['attribute', 'класс', 'функция', 'type']

for w in my_words:
    try:
        bytes(w, 'ascii')
    except UnicodeEncodeError:
        print(f"Слово, которое, невозможно записать в байтовом типе: {w}")

