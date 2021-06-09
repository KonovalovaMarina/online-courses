from functools import wraps

from flask_login import current_user, login_required as login_required_base
from werkzeug.exceptions import abort


def login_required(func=None, roles=()):

    def _wrapper(func):
        @login_required_base
        @wraps(func)
        def _wrapped(*args, **kwargs):
            if roles and current_user.role not in roles:
                return abort(403, description="Access Dnied")
            return func(*args, **kwargs)
        return _wrapped

    if func is None:
        return _wrapper

    return _wrapper(func)

