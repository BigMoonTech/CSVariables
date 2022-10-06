import re
from uuid import uuid4
from datetime import datetime
from typing import Optional
import src.db_models.db_session as db_session
from src.db_models.users import User
from src.db_models.completions import Completion
from src.db_models.unregistered_users import UnregisteredUser
from passlib.handlers.sha2_crypt import sha256_crypt as crypto
from logging import getLogger

logger = getLogger(__name__)


def find_user_by_email(email: str) -> Optional[User]:
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    session.close()
    return user


def create_user(name: str, email: str, password: str) -> Optional[User]:
    if find_user_by_email(email):
        return None

    user = User()
    user.uuid = uuid4().hex

    # check for a collision in the uuid
    while find_user_by_uuid(user.uuid):
        # log the collision
        logger.warning(f'Collision when generating a uuid: {user.uuid}')
        # if there is a collision, generate a new uuid
        user.uuid = uuid4().hex

    logger.info(f'Generated a new uuid: {user.uuid}')

    user.name = name
    user.email = email
    user.hashed_pw = hash_text(password)
    user.allowed_monthly_calls = 100
    user.calls_made = 0
    user.remaining_monthly_calls = 100

    session = db_session.create_session()
    session.add(user)
    session.commit()
    session.close()
    return user


def update_registered_user_calls(user_id: str):
    """ Update the number of calls made by a registered user """
    session = db_session.create_session()
    user = session.query(User).filter(User.uuid == user_id).first()
    if user:
        user.calls_made += 1
        user.remaining_monthly_calls -= 1
        session.commit()

    # todo: reset the number of calls made if the month has changed

    session.close()
    return user if user else None


def create_unregistered_user(ip_address: str) -> Optional[UnregisteredUser]:
    """ Handle the case where a user has not registered """
    session = db_session.create_session()
    _user = session.query(UnregisteredUser).filter(UnregisteredUser.ip_address == ip_address).count()
    if _user == 0:
        print('Creating new unregistered user')
        _user = UnregisteredUser()
        _user.ip_address = ip_address
        _user.free_calls = 3
        _user.calls_made = 0
        _user.remaining_calls = 3
        session.add(_user)
        session.commit()
    session.close()
    return _user if _user else None


def update_unregistered_user_calls(ip_address: str) -> Optional[UnregisteredUser]:
    """ Update the number of calls made by an unregistered user """
    session = db_session.create_session()
    _user = session.query(UnregisteredUser).filter(UnregisteredUser.ip_address == ip_address).first()
    if _user:
        _user.calls_made += 1
        _user.remaining_calls -= 1
        session.commit()
        session.close()
    return _user if _user else None


def hash_text(text: str) -> str:
    """ Hash a user's password """
    hashed_text = crypto.encrypt(text, rounds=171204)
    return hashed_text


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    """ Verify a user's password """
    return crypto.verify(plain_text, hashed_text)


def update_password(user_id: str, password: str) -> tuple[None, str] | tuple[User, None]:
    """
    Update a user's password.

    :param user_id: The user's uuid
    :param password: The user's new password
    :return: A tuple containing the user and None if successful, or None and an error message if not
    """

    # todo: move this password validation to the view model
    if not validate_password(password):
        error = 'Check password requirements... At least 6 characters, one number, ' \
                'one letter, only the special characters: !@.-_'
        return None, error

    session = db_session.create_session()
    user = session.query(User).filter(User.uuid == user_id).first()
    if user:
        user.hashed_pw = hash_text(password)
        session.commit()
        session.close()
        return user, None
    else:
        session.close()
        return None, 'User not found'


def validate_password(password: str) -> bool:
    """ Validate a user's password """
    # regex pattern to check if password is valid (6 characters, a number, a letter, and only !@.-_ allowed)
    password_requirements = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@.-_]{6,}$'
    if not re.match(password_requirements, password):
        return False
    return True


def update_email(user_id: str, new_email: str) -> Optional[User]:
    session = db_session.create_session()
    user = session.query(User).filter(User.uuid == user_id).first()
    if not user:
        return None

    user.email = new_email
    session.commit()
    session.close()
    return user


def login_user(email: str, password: str) -> Optional[User]:
    """ Login a user """
    session = db_session.create_session()

    user = session.query(User).filter(User.email == email).first()
    if not user or not verify_hash(user.hashed_pw, password):
        session.close()
        return None

    # update the user's last login time
    user.last_login = datetime.utcnow()
    session.commit()
    session.close()
    return user


def find_user_by_uuid(user_id: str) -> Optional[User]:
    """ Find a user by their uuid """
    if user_id is None:
        return None

    session = db_session.create_session()
    user = session.query(User).filter(User.uuid == user_id).first()
    session.close()

    if user is None:
        return None

    return user


def get_total_requests():
    """ Display the total number of requests made by all users """
    session = db_session.create_session()
    count = session.query(Completion).count()
    session.close()
    return count


def get_unregistered_user_by_ip(ip_address: str):
    """ Get the unregistered user by their IP address """

    if ip_address is None:
        print('No IP address given')
        return None

    session = db_session.create_session()
    query = session.query(UnregisteredUser).filter(UnregisteredUser.ip_address == ip_address).first()
    # raise exception if user no results from query
    if query is None:
        print('the query is:', query)
        session.close()
        return None

    session.close()
    return query


def update_email_confirmation(email: str, confirmed: bool = False) -> Optional[User]:
    """ Update the email confirmed status of a user """
    try:
        if not email.strip():
            return None
    except AttributeError:
        return None

    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return None

    if confirmed:
        user.confirmed = 1
        user.confirmed_on = datetime.utcnow()
    else:
        user.confirmed = 0
        user.confirmed_on = None

    session.commit()
    session.close()
    return user
