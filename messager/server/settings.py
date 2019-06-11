from os import path as osp

INSTALLED_APPS = [
    'users',
    'echo',
    'messager',
]

DATABASE = {
    'engine': 'sqlite',
    'path': osp.abspath(osp.join(osp.dirname(__file__), 'db.sqlite')),
}