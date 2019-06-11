import time


def validate_request(raw):
    if 'time' in raw and 'action' in raw:
        return True
    return False


def make_response(request, code, data=None):
    return {
        'action': request['action'],
        'user': request.get('user'),
        'time': time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(time.time())),
        'data': data,
        'code': code,
    }
