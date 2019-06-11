from pony import orm
from datetime import datetime
from db import db

model_names = ['Message', ]


class Message(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    time = orm.Required(datetime)
    text = orm.Required(str)
    user_from = orm.Required('User', reverse='out_messages')
    user_to = orm.Required('User', reverse='in_messages')

    def __str__(self):
        return f'<Message "{self.user_from}" => "{self.user_to}" {self.time}>'
