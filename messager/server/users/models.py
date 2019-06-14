from pony import orm
from datetime import datetime
from server.db import db

model_names = ['User', ]


class User(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    login = orm.Required(str, unique=True)
    pswdhash = orm.Required(str)
    last_login = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    out_messages = orm.Set('Message', reverse='user_from')
    in_messages = orm.Set('Message', reverse='user_to')

    def __str__(self):
        return f'<User "{self.login}">'
