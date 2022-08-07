"""
    2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
    Написать скрипт, автоматизирующий его заполнение данными. Для этого:

    Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
    цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря
    в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
    Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
import json

def write_order_to_json(item, quantity, price, buyer, date):
    my_dict = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date}
    print(my_dict)

    with open('orders.json', 'r') as rmf:
        r_content = rmf.read()
        obj = json.loads(r_content)

    obj['orders'].append(my_dict)

    with open('orders.json', 'w') as mf:
        mf.write(json.dumps(obj))


write_order_to_json('car', 6, 788350, 'ivan', '04.08.2022')

# {"orders": []}