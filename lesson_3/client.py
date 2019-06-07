from socket import *
import re
import time
from json import dumps, loads

# request     - объект запроса пользователя
# response    - объект ответа сервера на запрос пользователя

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 8888))

print('Запуск клиентской части мессенджера')

flag = True
prompt = '>'
re_echo = re.compile(r'^\.echo +')

def get_inp():
    return input(f'{prompt} ')

while flag:
    inp = get_inp()
    
    if len(inp)>0 and inp[0] == ".":   #режим ввода команд
        cmd = inp.split(" ")[0]
        if cmd == ".echo":
            request = {
                "action": "echo",
                "time": time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(time.time())),
                "message": re_echo.sub('',inp),
            }
        elif cmd == '.quite':
            flag == False
            continue
    
    s.send(dumps(request,ensure_ascii=False).encode('utf-8'))
    response = loads(s.recv(1_000_000).decode('utf-8'))
    if response['response'] == 200:
        if (cmd == '.echo') and ('message' in request):
            print(f'%server {response["time"]}\n>>>\t{response["message"]}')

s.close()