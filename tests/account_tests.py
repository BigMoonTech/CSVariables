from unittest.mock import patch

from flask import Response

from src.db_models.users import User
from test_client import flask_app


def test_view_register_post_successful_and_redirects_to_unconfirmed(client):
    from src.views.account_views import register_post
    form_data = {
        'name': 'Joshua',
        'email': 'test@afakeemail.com',
        'password': 'asd123'
    }
    target = 'src.services.user_service.find_user_by_email'
    find_user = patch(target, return_value=None)
    target = 'src.services.user_service.create_user'
    fake_user = User()
    fake_user.uuid = '1234'
    create_user = patch(target, return_value=fake_user)
    request = flask_app.test_request_context(path='/account/register', data=form_data)

    with find_user, create_user, request:
        resp: Response = register_post()

    assert resp.status_code == 302
    assert resp.location == '/unconfirmed'


def test_viewmodel_register_validation_passed_with_good_data(client):
    from src.view_models.account.register_viewmodel import RegisterViewModel
    form_data = {
        'name': 'Joshua',
        'email': 'test@afakeemail.com',
        'password': 'asd123'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()

    target = 'src.services.user_service.find_user_by_email'
    with patch(target, return_value=None):
        vm.validate()

    assert vm.error is None


def test_viewmodel_register_validation_fails_with_bad_data(client):
    from src.view_models.account.register_viewmodel import RegisterViewModel
    form_data = {
        'name': 'AVERYLONGNAMETHATISWAYTOOLONGTOBEVALID',
        'email': 'test@afakeemail.com',
        'password': 'asd123'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()
        vm.validate()

        assert vm.error is not None
        assert 'Name' in vm.error

    form_data = {
        'name': 'Good Name',
        'email': 'test@afakeemail.com',
        'password': 'asd asd'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()
        vm.validate()

        assert vm.error is not None
        assert 'password requirements' in vm.error


def test_viewmodel_register_fails_when_user_already_exists(client):
    from src.view_models.account.register_viewmodel import RegisterViewModel
    form_data = {
        'name': 'Good Name',
        'email': 'test@afakeemail.com',
        'password': 'Asd123'
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()

    target = 'src.services.user_service.find_user_by_email'
    with patch(target, return_value=User(email=form_data['email'])):
        vm.validate()

    assert vm.error is not None
    assert 'already exists' in vm.error

