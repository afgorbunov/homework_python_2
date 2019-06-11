from functools import reduce

from settings import INSTALLED_APPS


def get_server_actions():
    modules = reduce(  # получение списка приложений из INSTALLED_APPS
        lambda value, item: value + [__import__(f'{item}.actions')],
        INSTALLED_APPS,
        [],
    )
    actions = reduce(  # получение списка модулей actions из списка модулей приложений
        lambda value, item: value + [getattr(item, 'actions', [])],
        modules,
        [],
    )
    return reduce(  # получение списка активностей из модулей actions приложений
        lambda value, item: value + getattr(item, 'action_names', []),
        actions,
        [],
    )


def resolve(action_name, actions=None):
    if actions is None:
        actions = get_server_actions()
    action_mapping = {act['action']: act['controller'] for act in actions}
    if action_name in action_mapping.keys():
        return action_mapping[action_name]
    else:
        return None
