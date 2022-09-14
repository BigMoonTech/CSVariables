import re
from datetime import datetime
from typing import Optional

import src.db_models.db_session as db_session
from src.db_models.users import User
from src.db_models.completions import Completion
from src.db_models.unregistered_users import UnregisteredUser
from passlib.handlers.sha2_crypt import sha256_crypt as crypto


def find_user_by_email(email: str) -> Optional[User]:
    session = db_session.create_session()
    return session.query(User).filter(User.email == email).first()


def create_user(name: str, email: str, password: str) -> Optional[User]:
    if find_user_by_email(email):
        return None

    user = User()
    user.name = name
    user.email = email

    # regex pattern to check if password is valid (6 characters, a number, a letter, and only !@#%& allowed)
    password_requirements = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#%&]{6,}$'
    if not re.match(password_requirements, password):
        return None

    user.hashed_pw = hash_text(password)
    user.allowed_monthly_calls = 100
    user.calls_made = 0
    user.remaining_monthly_calls = 100

    session = db_session.create_session()
    session.add(user)
    session.commit()

    return user


def update_registered_user_calls(user_id: int):
    """ Update the number of calls made by a registered user """
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
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


def login_user(email: str, password: str) -> Optional[User]:
    """ Login a user """
    session = db_session.create_session()

    user = session.query(User).filter(User.email == email).first()
    if not user or not verify_hash(user.hashed_pw, password):
        user = None
    if user is None:
        session.close()
        return None

    # update the user's last login time
    user.last_login = datetime.now()
    session.commit()
    session.close()
    return user


def find_user_by_id(user_id: int) -> Optional[User]:
    """ Find a user by their ID """
    if user_id is None:
        return None

    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
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
