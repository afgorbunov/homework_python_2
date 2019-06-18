from decorators import logger_required, login_required

from protocol import make_response


@login_required
@logger_required
def get_echo(request, db=None):
    return make_response(request,200,request['data'])
