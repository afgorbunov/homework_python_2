from functools import reduce

from pony import orm

from settings import DATABASE, INSTALLED_APPS

db = orm.Database()
if DATABASE['engine'] == 'sqlite':
    db.bind(provider='sqlite', filename=DATABASE['path'], create_db=True)


pkgs = reduce(  # получение списка приложений из INSTALLED_APPS
    lambda value, item: value + [__import__(f'{item}.models')],
    INSTALLED_APPS,
    [],
)
modules = reduce(  # получение списка модулей models из списка модулей приложений
    lambda value, item: value + [getattr(item, 'models', [])],
    pkgs,
    [],
)
mod_names = reduce(  # получение списка имен классов моделей
    lambda value, item: value + getattr(item, 'model_names', []),
    modules,
    [],
)

classes = dict()  # словарь с классами моделей

for cn in mod_names:
    for m in modules:
        if cn in m.__dict__:
            classes[cn] = m.__dict__[cn]

print(classes)
db.generate_mapping(create_tables=True)
