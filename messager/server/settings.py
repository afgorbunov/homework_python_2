from os import path as osp
import logging

ENCODING = 'utf-8'

INSTALLED_APPS = [
    'users',
    'echo',
    'messager',
]

DATABASE = {
    'engine': 'sqlite',
    'path': osp.abspath(osp.join(osp.dirname(__file__), 'db.sqlite')),
}

LOGGER = {
    'level': logging.DEBUG,
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'path': 'main.log',
    'encoding': ENCODING,
}
