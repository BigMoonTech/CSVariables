from flask import Blueprint, redirect
from src.infrastructure.view_modifier import response
import src.infrastructure.cookie_auth as cookie_auth
from src.services import user_service
from src.view_models.account.register_viewmodel import RegisterViewModel
from src.view_models.account.login_viewmodel import LoginViewModel
from src.view_models.account.index_viewmodel import IndexViewModel
from src.view_models.account.history_viewmodel import HistoryViewModel
from src.view_models.account.update_viewmodel import UpdateViewModel
from src.view_models.shared.viewmodel_base import ViewModelBase

blueprint = Blueprint('account', __name__, template_folder='templates')

# ################### HISTORY ####################################


@blueprint.route('/account/history', methods=['GET'])
@response(template_file='account/history.html')
def history():
    # todo: complete the history page
    viewmodel = HistoryViewModel()
    viewmodel.validate()

    if viewmodel.user_id is None:
        return redirect('/account/login')

    return viewmodel.to_dict()


# ################### INDEX ####################################


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    # todo: complete the account index page
    viewmodel = IndexViewModel()

    if viewmodel.user_id is None:
        return redirect('/account/login')

    return viewmodel.to_dict()


# ################### REGISTER #################################


@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    viewmodel = RegisterViewModel()
    if viewmodel.user_id:
        return redirect('/app')
    return viewmodel.to_dict()


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    viewmodel = RegisterViewModel()
    viewmodel.validate()

    if viewmodel.error:
        return viewmodel.to_dict()

    user = user_service.create_user(viewmodel.name, viewmodel.email, viewmodel.password)
    if not user:
        viewmodel.error = 'The account could not be created.'
        return viewmodel.to_dict()

    resp = redirect('/app')
    cookie_auth.set_auth(resp, user.uuid)

    return resp


# ################### LOGIN ####################################


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    viewmodel = LoginViewModel()

    # if user is already logged in, redirect to account index page
    if viewmodel.user_id:
        return redirect('/app')

    return viewmodel.to_dict()


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    viewmodel = LoginViewModel()
    viewmodel.validate()

    if viewmodel.error:
        return viewmodel.to_dict()

    user = user_service.login_user(viewmodel.email, viewmodel.password)

    if user is None:
        viewmodel.error = 'Invalid email or password.'
        return viewmodel.to_dict()

    resp = redirect('/app')
    cookie_auth.set_auth(resp, user.uuid)
    return resp


# ################### LOGOUT ###################################


@blueprint.route('/account/logout')
def logout():
    resp = redirect('/')
    cookie_auth.logout(resp)
    return resp


# ################### PASSWORD RESET ###################################


@blueprint.route('/account/password_reset', methods=['GET'])
def password_reset_get():
    resp = redirect('/')
    return resp


@blueprint.route('/account/password_reset', methods=['POST'])
def password_reset_post():
    # todo: complete the password reset page
    resp = redirect('/')
    return resp


# ################### PASSWORD CHANGE ###################################


@blueprint.route('/account/change_password', methods=['GET'])
@response(template_file='account/change_password.html')
def change_password_get():
    viewmodel = ViewModelBase()

    if viewmodel.user_id is None:
        return redirect('/account/login')

    return viewmodel.to_dict()


@blueprint.route('/account/change_password', methods=['POST'])
@response(template_file='account/change_password.html')
def change_password_post():
    viewmodel = UpdateViewModel()
    viewmodel.validate()

    # check for errors in the form
    if viewmodel.error:
        return viewmodel.to_dict()

    # update the user's password
    password_change = user_service.update_password(viewmodel.user_id, viewmodel.new_password)
    if not password_change[0]:
        viewmodel.error = password_change[1]
        return viewmodel.to_dict()

    return redirect('/account')


# ################### EMAIL CHANGE ###################################


@blueprint.route('/account/change_email', methods=['GET'])
@response(template_file='account/change_email.html')
def change_email_get():
    viewmodel = IndexViewModel()
    viewmodel.validate()

    return viewmodel.to_dict()


@blueprint.route('/account/change_email', methods=['POST'])
@response(template_file='account/change_email.html')
def change_email_post():
    viewmodel = IndexViewModel()
    viewmodel.validate()

    if viewmodel.error:
        return viewmodel.to_dict()

    if user is None:
        viewmodel.error = 'Invalid email or password.'
        return viewmodel.to_dict()

    resp = redirect('/app')
    cookie_auth.set_auth(resp, user.uuid)
    return resp
