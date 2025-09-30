from functools import wraps

from flask_jwt_extended import  get_jwt
from werkzeug.exceptions import Forbidden


def role_required(allowed_roles: list[str]):
    """
    Decorator to restrict access to users with specific roles.
    Args:
        allowed_roles (list[str]): List of allowed roles (e.g., ["Admin", "Doctor"]).

    Raises:
        Forbidden: If the user's role is not in allowed_roles.

    Returns:
        function: Wrapped function with role-based access control.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()

            if claims.get('role') not in allowed_roles:
                raise Forbidden('You don\'t have access to this resource')

            return fn(*args, **kwargs)
        return wrapper

    return decorator