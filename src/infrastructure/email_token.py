from typing import Optional

from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token: str, expiration: int = 3600) -> Optional[str]:
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
        return email
    # todo: Broader exception handling, and logging
    except:
        return None
