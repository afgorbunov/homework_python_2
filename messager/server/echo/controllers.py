from server.protocol import make_response


def get_echo(request, db=None):
    return make_response(request,200,request['data'])