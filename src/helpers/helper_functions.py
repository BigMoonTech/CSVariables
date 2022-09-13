""" A small library of helper functions. """
from typing import Optional

from requests import get


def try_int(text) -> int:
    try:
        return int(text)
    except:
        return 0


def get_ip_address() -> Optional[str]:
    try:
        ip = get('https://api.ipify.org').text
        print(f'User IP: {ip}')
        return ip

    # todo: add more specific exceptions
    except:
        return None
