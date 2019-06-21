from socket import *
import re
from datetime import datetime
from json import dumps, loads
from argparse import ArgumentParser
import zlib

# request     - объект запроса пользователя
# response    - объект ответа сервера на запрос пользователя

parser = ArgumentParser()
parser.add_argument(
    '-m', '--mode', type=str, default='w',
    help='Установка режима клиента'
)

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 8888))

print('Запуск клиентской части мессенджера')

flag = True
prompt = '>'
re_echo = re.compile(r'^\.echo +')
re_reg = re.compile(r'^\.reg +')
user = ''

def get_inp():
    return input(f'{prompt} ')

def get_timestamp():
    return str(datetime.now())

while flag:
    inp = get_inp()

    if len(inp) > 0 and inp[0] == '.':  # режим ввода команд
        cmd = inp.split(' ')[0]
        if cmd == '.echo':
            request = {
                'action': 'echo',
                'time': get_timestamp(),
                'data': re_echo.sub('', inp),
            }
        elif cmd == '.reg':
            request = {
                'action': 'reg',
                'time': get_timestamp(),
                'data': re_reg.sub('', inp),
            }
        elif cmd == '.login':
            request = {
                'action': 'login',
                'time': get_timestamp(),
                'user': inp.split(' ')[1],
                'data': inp.split(' ')[2],
            }
        elif cmd == '.quite':
            flag == False
            continue
    elif len(inp) > 0 and inp[0] == '@':
        to = inp.split(' ')[0]
        request = {
            'action': 'private_message',
            'user': user,
            'to': to,
            'data': inp.split(' ')[1],
            'time': get_timestamp(),
        }

    b_request = zlib.compress(dumps(request, ensure_ascii=False).encode('utf-8'))
    s.send(b_request)
    response = loads(zlib.decompress(s.recv(1_000_000)).decode('utf-8'))
    if response['code'] == 200:
        if (cmd == '.echo') and ('data' in request):
            print(f'%server {response["time"]}\n>>>\t{response["data"]}')
        if (cmd == '.reg') and ('data' in request):
            user = response['user']
        if (cmd == '.login')  and ('data' in request):
            print(response)
    print('response:', response)

s.close()
