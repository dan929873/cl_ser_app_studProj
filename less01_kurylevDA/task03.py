# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
# байтовом типе.

my_words = ['attribute', 'класс', 'функция', 'type']

for w in my_words:
    print(w.encode('utf-8'))

# attribute, type - невозможно записать в байтовом типе.