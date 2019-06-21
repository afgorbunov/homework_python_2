import json
import logging
import zlib
from urllib import response

from protocol import make_response
from settings import LOGGER

logging.basicConfig(
    level = LOGGER['level'],
    format = LOGGER['format'],
    handlers=[
        logging.FileHandler(LOGGER['path'], encoding=LOGGER['encoding']),
        logging.StreamHandler(),
    ]
)


def compression_middleware(func):
    def wrapper(request, *args, **kwargs):
        b_request = zlib.decompress(request)
        b_response = func(b_request, *args, **kwargs)
        return zlib.compress(b_response)
    return wrapper

def loggind_middleware(func):
    def wrapper(request, *args, **kwargs):
        try:
            json_response = func(request, *args, **kwargs)
            response = json.loads(json_response.decode())
        except Exception as err:
            response = make_response(request,500, 'Внутренняя ошибка сервера')
            logging.critical(err)
        if response['code'] == 400 or response['code'] == 404:
            logging.error(f'Обработка действия {request["action"]} была '
                f'возвращена ошибка с кодом {request["code"]}')
        return json_response
    return wrapper
