from socket import *
import re
import time
from json import dumps, loads

# request     - объект запроса пользователя
# response    - объект ответа сервера на запрос пользователя

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 8888))
s.listen(5)

print('Запуск серверной части мессенджера')

flag = True

while flag:
    client, addr = s.accept()
    
    request = loads(client.recv(1_000_000).decode('utf-8'))
    if 'action' in request.keys():
        if request['action'] == 'echo':
            response = {
                'response': 200,
                'time': time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(time.time())),
                'message': request['message'],
            }

    client.send(dumps(response,ensure_ascii=False).encode('utf-8'))
    client.close()
