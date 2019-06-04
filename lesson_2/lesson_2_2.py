# -*- coding: utf-8 -*-

# Практическая работа

# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате
# JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение
# данными. Для этого:
#     a. Создать функцию write_order_to_json(), в которую передается 5 параметров
#     — товар (item), количество (quantity), цена (price), покупатель (buyer),
#     дата (date). Функция должна предусматривать запись данных в виде словаря
#     в файл orders.json. При записи данных указать величину отступа в 4
#     пробельных символа;
#     b. Проверить работу программы через вызов функции write_order_to_json()
#     с передачей в нее значений каждого параметра.
# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт,
# автоматизирующий сохранение данных в файле YAML-формата. Для этого:
#     a. Подготовить данные для записи в виде словаря, в котором первому ключу
#     соответствует список, второму — целое число, третьему — вложенный словарь,
#     где значение каждого ключа — это целое число с юникод-символом,
#     отсутствующим в кодировке ASCII (например, €);
#     b. Реализовать сохранение данных в файл формата YAML — например, в файл
#     file.yaml. При этом обеспечить стилизацию файла с помощью параметра
#     default_flow_style, а также установить возможность работы с юникодом:
#     allow_unicode = True;
#     c. Реализовать считывание данных из созданного файла и проверить,
#     совпадают ли они с исходными.

# Необходимые и достаточные условия

#     1. Реализовать скрипт для чтения/записи данных в формате csv;
#     2. Реализовать скрипт для чтения/записи данных в формате json;
#     3. Реализовать скрипт для чтения/записи данных в формате yaml;
#     4. Реализовать скрипт для преобразования данных в формате csv в формат json;
#     5. Реализовать скрипт для преобразования данных в формате csv в формат yaml;
#     6. Реализовать скрипт для преобразования данных в формате json в формат yaml.


import os
import re
from copy import deepcopy
from csv import DictReader, DictWriter
from datetime import datetime
from json import dump as jdump
from os import path as osp
from time import strptime

from yaml import dump as ydump


class Converter():
    def __init__(self, filename):
        self.path = filename
        self.data = list()
        if osp.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as csvfl:
                for row in DictReader(csvfl.readlines(), delimiter=';'):
                    dt = dict()
                    for k,v in dict(row).items():
                        if v.isdigit():
                            dt[k] = int(v)
                        elif re.match(r'^\d+\.\d+$',v) is not None:
                            dt[k] = float(v)
                        else:
                            dt[k] = v
                    self.data.append(dt)
        else:
            raise FileNotFoundError(f'Путь "{self.path}" не обнаружен.')
        self.struct_data = dict()
        self.goods = dict()
        for row in self.data:
            if row['покупатель'] not in self.struct_data:
                self.struct_data[row['покупатель']] = list()
            if row['товар'] not in self.goods:
                self.goods[row['товар']] = {
                    'название':row['товар'],
                    'цена':row['цена'],
                }
            self.struct_data[row['покупатель']].append({
                'дата': row['дата'],
                'товар': self.goods[row['товар']],
                'количество': row['количество'],
                'сумма': self.goods[row['товар']]['цена'] * row['количество'],
            })


    def write_to_json(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as wfl:
            jdump(self.struct_data, wfl,
                 ensure_ascii=False, indent=4, sort_keys=True)
        pass

    def write_to_yaml(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as wfl:
            ydump(self.struct_data,wfl,indent=4, allow_unicode=True)
        pass
    def pprint(self):
        print(self.struct_data)


if __name__ == '__main__':
    datapath = osp.abspath(osp.join(osp.dirname(__file__), 'data'))
    cnv = Converter(osp.join(datapath,'orders.csv'))
    cnv.write_to_json(osp.join(datapath, 'orders.json'))
    cnv.write_to_yaml(osp.join(datapath, 'orders.yaml'))
