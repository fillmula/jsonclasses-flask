from flask import request, g, current_app
from werkzeug.exceptions import Unauthorized
from jwt import DecodeError
from .decode_jwt_token import decode_jwt_token


async def set_operator():
    if 'authorization' not in request.headers:
        g.current_user = None
        return
    authorization = request.headers['authorization']
    token = authorization[7:]
    try:
        decoded = decode_jwt_token(token)
    except DecodeError:
        raise Unauthorized('Authorization token is invalid.')
    operator_id = decoded['operator_id']
    operator_cls = current_app.config['operator_cls']
    operator = await operator_cls.id(operator_id)
    g.operator = operator
