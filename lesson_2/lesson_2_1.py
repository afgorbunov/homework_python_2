# -*- coding: utf-8 -*-

# Практическая работа

# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
# осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
# info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
#     a. Создать функцию get_data(), в которой в цикле осуществляется перебор
#     файлов с данными, их открытие и считывание данных. В этой функции из
#     считанных данных необходимо с помощью регулярных выражений извлечь
#     значения параметров «Изготовитель системы», «Название ОС», «Код продукта»,
#     «Тип системы». Значения каждого параметра поместить в соответствующий
#     список. Должно получиться четыре списка — например, os_prod_list,
#     os_name_list, os_code_list, os_type_list. В этой же функции создать главный
#     список для хранения данных отчета — например, main_data — и поместить в
#     него названия столбцов отчета в виде списка: «Изготовитель системы»,
#     «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов
#     также оформить в виде списка и поместить в файл main_data (также для
#     каждого файла);
#     b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
#     В этой функции реализовать получение данных через вызов функции get_data(),
#     а также сохранение подготовленных данных в соответствующий CSV-файл;
#     c. Проверить работу программы через вызов функции write_to_csv().

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
from csv import DictWriter
from json import dump as jdump
from yaml import dump as ydump
from os import path as osp


class DataString():
    def __init__(self, source):
        self.source = source
        self.data = dict()

    def add(self, caption, value):
        self.data[caption] = value

    def get_dict(self):
        return deepcopy(self.data)

    def get_csv(self, params_tuple, delimiter):
        return delimiter.join([self.data[p] for p in params_tuple])


class Data():
    def __init__(self, params):
        self.params = params
        self.strings = list()
        self.regexps = {p: re.compile(f'{p}: +') for p in params}

    def add(self, source):
        self.strings.append(DataString(source))
        with open(source, 'r', encoding='cp1251') as dtf:
            for line in dtf.readlines():
                for p in self.params:
                    if not self.regexps[p].match(line) is None:
                        self.strings[-1].add(p, self.regexps[p].split(line)
                                             [1].replace('\n', ''))

    def get_csv(self, delimiter):
        csv = delimiter.join(self.params) + '\n'
        for ds in self.strings:
            csv += ds.get_csv(tuple(self.params), delimiter) + '\n'
        return csv

    def get_dicts(self):
        return [ds.get_dict() for ds in self.strings]


class Converter():
    def __init__(self, dirpath, params):
        self.path = dirpath
        self._files = list()
        self.params = params
        self.data = Data(self.params)

    def get_data_from_txt(self):
        if osp.exists(self.path):
            self._files = [osp.abspath(osp.join(self.path, f)) for f in os.listdir(
                self.path) if osp.isfile(osp.join(self.path, f)) and osp.splitext(f)[1] == '.txt']
            for fl in self._files:
                self.data.add(fl)
        else:
            raise FileNotFoundError(f'Путь "{self.path}" не обнаружен.')

    def write_to_csv(self, filepath, delimiter=';', way='native'):
        with open(filepath, 'w', encoding='utf-8') as wfl:
            if way == 'native':
                wfl.write(self.data.get_csv(delimiter))
            elif way == 'module':
                writer = DictWriter(wfl, delimiter=delimiter,
                                    fieldnames=self.params)
                writer.writeheader()
                for d in self.data.get_dicts():
                    writer.writerow(d)
            wfl.flush()

    def write_to_json(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as wfl:
            jdump(self.data.get_dicts(), wfl,
                 ensure_ascii=False, indent=4, sort_keys=True)

    def write_to_yaml(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as wfl:
            ydump(self.data.get_dicts(),wfl,indent=2, allow_unicode=True)



if __name__ == '__main__':
    datapath = osp.abspath(osp.join(osp.dirname(__file__), 'data'))
    cnv = Converter(datapath, [
        'Изготовитель системы',
        'Название ОС',
        'Код продукта',
        'Тип системы',
    ])
    cnv.get_data_from_txt()
    cnv.write_to_csv(osp.join(datapath, 'data.csv'), way='module')
    cnv.write_to_json(osp.join(datapath, 'data.json'))
    cnv.write_to_yaml(osp.join(datapath, 'data.yaml'))
