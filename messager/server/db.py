from functools import reduce

from pony import orm

from server.settings import DATABASE, INSTALLED_APPS

db = orm.Database()
if DATABASE['engine'] == 'sqlite':
    db.bind(provider='sqlite', filename=DATABASE['path'], create_db=True)

serv_pkg = __import__('server')
print(serv_pkg)
pkgs = reduce(  # получение списка приложений из INSTALLED_APPS
    lambda value, item: value + [getattr(serv_pkg, item, [])],
    INSTALLED_APPS,
    [],
)
print(pkgs)
for k,v in pkgs[0].__dict__.items():
    print(f'\t{k}:\t{v}')
modules = reduce(  # получение списка модулей models из списка модулей приложений
    lambda value, item: value + [getattr(item, 'models', [])],
    pkgs,
    [],
)
print(modules)
mod_names = reduce(  # получение списка имен классов моделей
    lambda value, item: value + getattr(item, 'model_names', []),
    modules,
    [],
)
print(mod_names)

classes = dict()  # словарь с классами моделей

for cn in mod_names:
    for m in modules:
        if cn in m.__dict__:
            classes[cn] = m.__dict__[cn]

print(classes)
db.generate_mapping()
