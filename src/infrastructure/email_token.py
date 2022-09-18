from typing import Optional

from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token: str, expiration: int = 3600) -> Optional[str]:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )

    # todo: Broader exception handling, and logging
    except:
        return None
    return email
