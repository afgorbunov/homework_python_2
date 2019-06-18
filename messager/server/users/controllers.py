from datetime import datetime

from pony.orm import commit, db_session, select

from protocol import make_response


def _get_login_pair(request):
    return request.get('data').split(' ')

def get_523(request):
    return make_response(request, 523, data='Хранилище не обнаружено')

@db_session
def set_user(request, db=None):
    login_pair = _get_login_pair(request)
    if db:
        user = db.User(
            login=login_pair[0], 
            pswdhash=login_pair[1], 
            last_login=datetime.now(),
        )
        commit()
        request['user'] = user.login
        return make_response(request, 201, data='Пользователь зарегестрирован')
    else:
        return get_523(request)

@db_session
def login(request, db=None):
    if db:
        user = db.User.get(login =request.get('user'))
        if user.pswdhash == request.get('data'):
            return make_response(request, 200, data=f"Пользователь '{user.login}' авторизован")
        else:
            return make_response(request, 401, data=f"Неверное имя пользователя и/или пароль")
    else:
        return get_523(request)
