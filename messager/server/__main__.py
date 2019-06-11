import re
import time
from json import dumps, loads
from socket import *

from actions import resolve
from protocol import validate_request, make_response
from db import db

# request     - объект запроса пользователя
# response    - объект ответа сервера на запрос пользователя

flag = True
host = '0.0.0.0'
port = 8888
buffer_size = 1_000_000
encoding = 'utf-8'

s = socket(AF_INET, SOCK_STREAM)
s.bind((host, port))
print(f'Запуск серверной части мессенджера с параметрами: {host}:{port}')
s.listen(5)

try:
    while flag:
        client, addr = s.accept()

        request = loads(client.recv(buffer_size).decode(encoding))
        if validate_request(request):
            controller = resolve(request['action'])
            if controller:
                try:
                    response = controller(request, db=db)
                except Exception as err:
                    print(err)
                    response = make_response(
                        request, 500, 'Внутренняя ошибка сервера')
            else:
                response = make_response(request, 404, "Действие не найдено")
        else:
            response = make_response(request, 400, "Некорректный запрос")

        client.send(dumps(response, ensure_ascii=False).encode(encoding))
        client.close()
except KeyboardInterrupt:
    pass
