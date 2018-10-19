from flask import request
from app.models import Students


def check_is_login():
    token = request.values.get('token', '')
    id = request.values.get('id', '')
    user = Students.query.filter_by(id=id).first()
    result = False
    if user is not None:
        result = user.confirm(token.encode())
    return result
