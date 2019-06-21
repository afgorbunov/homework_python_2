import logging
import re
import time
from json import dumps, loads
import select
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
s.setblocking(False)
print(f'Запуск серверной части мессенджера с параметрами: {host}:{port}')
s.listen(5)

requests = []
connections = []

try:
    while flag:
        try:
            client, addr = s.accept()
            logging.debug(f'Соединение клиента с адресом {addr}')
            connections.append(client)
        except:
            pass
        
        rlist, wlist, xlist = select.select(connections, connections, connections, 0)

        for rclient in rlist:
            b_request = rclient.recv(buffer_size)
            requests.append(b_request)
        
        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for wclient in wlist:
                wclient.send(b_response)

except KeyboardInterrupt:
    pass
