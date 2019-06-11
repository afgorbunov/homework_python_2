from .controllers import set_user, login

action_names = [
    {'action': 'reg', 'controller': set_user},
    {'action': 'login', 'controller': login},
]
