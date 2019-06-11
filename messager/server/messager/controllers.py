from datetime import datetime

from pony.orm import commit, db_session

from protocol import make_response


@db_session
def send_private_message(request, db=None):
    mes = db.Message(
        text = request.get('data'), 
        time = request.get('time'), 
        user_from = request.get('user'),
        user_to = request.get('to'),
    )
