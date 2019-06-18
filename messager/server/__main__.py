import logging
import re
import time
from json import dumps, loads
from socket import *
from zipfile import error

from actions import resolve
from db import db
from handlers import handle_default_request
from protocol import make_response, validate_request
from settings import LOGGER, ENCODING

# request     - объект запроса пользователя
# response    - объект ответа сервера на запрос пользователя

flag = True
host = '0.0.0.0'
port = 8888
buffer_size = 1_000_000


logging.basicConfig(
    level = LOGGER['level'],
    format = LOGGER['format'],
    handlers=[
        logging.FileHandler(LOGGER['path'], encoding=LOGGER['encoding']),
        logging.StreamHandler(),
    ]
)

s = socket(AF_INET, SOCK_STREAM)
s.bind((host, port))
print(f'Запуск серверной части мессенджера с параметрами: {host}:{port}')
s.listen(5)

try:
    while flag:
        client, addr = s.accept()
        logging.debug(f'Соединение клиента с адресом {addr}')

        b_request = loads(client.recv(buffer_size))
        logging.debug(f'От клиента с адресом {addr} получен запрос с действием {request["action"]}')

        b_response = handle_default_request(b_request)

        client.send(dumps(response, ensure_ascii=False).encode(ENCODING))
        client.close()
except KeyboardInterrupt:
    pass
