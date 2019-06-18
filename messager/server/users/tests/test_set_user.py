from pytest import fixture
from pony import orm
from datetime import datetime

from server.users.controllers import set_user, login
# from server.users.models import User


server = __import__('server')
users = getattr(server, 'users')
model_module = getattr(users, 'models')
model = getattr(model_module, 'Users')


@fixture
def action_fixture():
    return 'reg'


@fixture
def time_fixture():
    return datetime.now().timestamp()


@fixture
def data_fixture():
    return 'some data'


@fixture
def db_fixture():
    db = orm.Database()
    db.bind(provider='sqlite', filename=':memory:')
    db.generate_mapping(create_tables=True)
    return db


@fixture
def request_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'time': time_fixture,
        'data': data_fixture,
    }


@fixture
def code_fixture():
    return 201


@fixture
def user_fixture():
    return 'some'


@fixture
def response_fixture(action_fixture, time_fixture, data_fixture):
    return {
        'action': action_fixture,
        'time': time_fixture,
        'data': data_fixture,
        'code': code_fixture,
        'user': user_fixture,
    }


@fixture
def test_set_user(request_fixture, db_fixture):
    response = set_user(request_fixture, db=db_fixture)
    assert response_fixture.get('code') == response.get('code')
