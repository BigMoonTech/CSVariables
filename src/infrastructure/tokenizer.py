from typing import Optional

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app


def generate_token(serializable_item: str) -> Optional[str]:
    """
    Takes a string and returns a token.

    :param serializable_item: The string to be serialized
    :return: The token or None
    """
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(serializable_item, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    except KeyError:
        current_app.logger.error('SECRET_KEY or SECURITY_PASSWORD_SALT not set in config')
        return None


def confirm_token(token: str, expiration: int = 3600) -> Optional[str]:
    """
    Takes a token and returns the original string, with a max expiration time of 1 hour.
    Raises KeyError if SECRET_KEY or SECURITY_PASSWORD_SALT not set in config.
    Raises TypeError if token is not a string.

    :param token: The token to be confirmed
    :param expiration: The max expiration time in seconds
    :return: The original string or None
    """

    # exception for token not being a string
    if not isinstance(token, str):
        current_app.logger.error('Token must be a string')
        raise TypeError('Token must be a string')

    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        deserialized_input = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
        return deserialized_input

    # exception for secret key not in config
    except KeyError:
        current_app.logger.error('SECRET_KEY or SECURITY_PASSWORD_SALT not set in config')
        raise KeyError

    # exception for token being expired
    except SignatureExpired:
        current_app.logger.error('Token is expired')

    # exception for token being invalid
    except BadSignature:
        current_app.logger.error('Validation failed.')

    return None
