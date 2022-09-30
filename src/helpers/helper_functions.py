""" A small library of helper functions. """
from typing import Optional

from requests import get


def get_ip_address() -> Optional[str]:
    try:
        ip = get('https://api.ipify.org').text
        print(f'User IP: {ip}')

        if ip is None or ip.strip() == '':
            return None
        return ip.strip()

    # todo: add more specific exceptions
    except:
        return None


# todo: look into how to use this decorator without using flask session
# def login_required(f):
#     """
#     Decorate routes to require login.
#
#     https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
#     """
#
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("user_id") is None:
#             return redirect("/login")
#         return f(*args, **kwargs)
#
#     return decorated_function
