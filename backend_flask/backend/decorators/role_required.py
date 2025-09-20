from functools import wraps
from flask_jwt_extended import  get_jwt
from werkzeug.exceptions import Forbidden


def role_required(allowed_roles: list[str]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()

            if claims.get('role') not in allowed_roles:
                raise Forbidden('You don\'t have access to this resource')

            return fn(*args, **kwargs)
        return wrapper

    return decorator