# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
# строкового представления в байтовое и выполнить обратное преобразование (используя
# методы encode и decode)

my_words = ['разработка', 'администрирование', 'protocol', 'standard']

for w in range(len(my_words)):
    my_words[w] = my_words[w].encode('utf-8')
    print(my_words[w])

    my_words[w] = my_words[w].decode('utf-8')
    print(my_words[w])