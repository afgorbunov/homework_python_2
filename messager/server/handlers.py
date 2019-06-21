import json
import logging

from actions import resolve
from db import db
from middlewares import compression_middleware, logging_middleware
from protocol import make_response, validate_request
from settings import ENCODING


@compression_middleware
@logging_middleware
def handle_default_request(raw_request):
    request = json.loads(raw_request.decode(ENCODING))
    logging.debug(f'Получен запрос с действием {request["action"]}')
    action_name = request.get('action')
    if validate_request(request):
        controller = resolve(request['action'])
        if controller:
            response = controller(request, db=db)
        else:
            response = make_response(request, 404, 'Действие не найдено')
    else:
        response = make_response(request, 400, 'Некорректный запрос')

    return json.dumps(response, ensure_ascii=False).encode(ENCODING)
