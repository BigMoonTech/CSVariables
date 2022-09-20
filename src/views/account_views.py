from flask import Blueprint, redirect, url_for, render_template, request, flash, current_app

from src.helpers.email import send_email
from src.infrastructure.email_token import confirm_token, generate_token
from src.infrastructure.view_modifier import response
import src.infrastructure.cookie_auth as cookie_auth
from src.services import user_service
from src.view_models.account.account_activation_viewmodel import ActivationViewModel
from src.view_models.account.pwd_reset_viewmodel import PasswordResetRequestViewModel, PasswordResetFormViewModel
from src.view_models.account.register_viewmodel import RegisterViewModel
from src.view_models.account.login_viewmodel import LoginViewModel
from src.view_models.account.index_viewmodel import IndexViewModel
from src.view_models.account.history_viewmodel import HistoryViewModel
from src.view_models.account.update_viewmodel import PwUpdateViewModel, EmailUpdateViewModel
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

    else:
        user = user_service.create_user(viewmodel.name, viewmodel.email, viewmodel.password)
        if not user:
            viewmodel.error = 'The account could not be created.'
            return viewmodel.to_dict()

        email_token = generate_token(viewmodel.email)
        viewmodel.confirm_url = url_for('account.confirm_email', token=email_token, _external=True)
        html = render_template('account/activate_account_email_contents.html', confirm_url=viewmodel.confirm_url)
        email_subject = 'Please Confirm Email'
        send_email(viewmodel.email, email_subject, html)

        resp = redirect('/unconfirmed')
        cookie_auth.set_auth(resp, user.uuid)
        return resp


# ################### EMAIL CONFIRMATION ####################################

@blueprint.route('/unconfirmed')
@response(template_file='account/email_unconfirmed.html')
def unconfirmed():
    viewmodel = ActivationViewModel()
    # todo - validate the unconfirmed view
    viewmodel.validate()

    if viewmodel.error:
        flash("That's not allowed.")
        return redirect('/account/login')

    if viewmodel.user.confirmed:
        return redirect('/app')

    flash('Please activate your account.')
    return viewmodel.to_dict()


@blueprint.route('/confirm/<token>', methods=['GET', 'POST'])
@response(template_file='account/confirm.html')
def confirm_email(token):
    viewmodel = ActivationViewModel()
    # todo: validate the confirm email view
    # todo: refactor this function (It has a bit of a code smell)

    try:
        email = confirm_token(token).lower()

        # if logged in, and if the token is valid then update the user's confirmed field
        if viewmodel.user_id:
            if viewmodel.user.email == email:
                user = user_service.update_email_confirmation(viewmodel.user.email, confirmed=True)
                if user:
                    return redirect('/app')
                else:
                    viewmodel.error = 'The account could not be confirmed.'
                    return viewmodel.to_dict()
            else:
                viewmodel.error = 'The email confirmation link is invalid or has expired.'
                return viewmodel.to_dict()

        # if not logged in, then get the user by email and update the user's confirmed field
        else:
            user = user_service.find_user_by_email(email)
            if user:
                if not user.confirmed:
                    user = user_service.update_email_confirmation(email, confirmed=True)
                    if user:
                        return redirect('/account/login')

                    print('Account confirmed. Please login.')
                    return viewmodel.to_dict()

                else:
                    viewmodel.error = 'Account already confirmed. Please login.'
                    return redirect('/account/login')
            else:
                viewmodel.error = 'There is no account associated with this email.'
                return redirect('/account/register')
    except:
        viewmodel.error = 'The confirmed link is invalid or has expired.'
        return redirect('/unconfirmed')


# ################### LOGIN ####################################


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    viewmodel = LoginViewModel()

    # if user is already logged in, and email verified, then redirect to app page
    if viewmodel.user_id:
        if viewmodel.user.confirmed:
            return redirect('/app')

        # if the user is logged in, but not confirmed, redirect to unconfirmed page
        return redirect('/unconfirmed')

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
@blueprint.route('/password_reset/<token>', methods=['GET'])
@response(template_file='account/password_reset_form.html')
def verified_password_reset_get(token):
    viewmodel = PasswordResetFormViewModel()
    viewmodel.token = confirm_token(token).lower()

    # token error handling and validation
    viewmodel.validate_token()
    if viewmodel.error:
        flash(viewmodel.error)
        current_app.logger.warning(f'Password reset token error: {viewmodel.error}, for user with token: {token}')
        return redirect('/account/login')

    return viewmodel.to_dict()


@blueprint.route('/password_reset/<token>', methods=['POST'])
@response(template_file='account/password_reset_form.html')
def verified_password_reset_post(token):
    viewmodel = PasswordResetFormViewModel()
    viewmodel.token = viewmodel.user_id = confirm_token(token).lower()

    # token error handling and validation
    viewmodel.validate_token()
    if viewmodel.error:
        flash(viewmodel.error)
        current_app.logger.warning(f'Password reset token error: {viewmodel.error}, for user with token: {token}')
        return redirect('/account/login')

    # validate the form inputs
    viewmodel.validate()
    if viewmodel.error:
        return viewmodel.to_dict()

    # update the user's password
    viewmodel.user = user_service.update_password(viewmodel.user_id, viewmodel.password)

    # if the password was updated, then redirect to the login page, else show password error
    if not viewmodel.user[0]:
        viewmodel.error = viewmodel.user[1]
        return viewmodel.to_dict()

    flash('Password reset successful. Please login using your new password.')
    return redirect('/account/login')


@blueprint.route('/password_reset', methods=['GET'])
@response(template_file='account/password_reset_request.html')
def password_reset_get():
    viewmodel = PasswordResetRequestViewModel()

    # if the user is logged in, then redirect to app page
    if viewmodel.user_id:
        flash('Password reset is only available to users who are not logged in.')
        return redirect('/app')

    return viewmodel.to_dict()


@blueprint.route('/password_reset', methods=['POST'])
@response(template_file='account/password_reset_request.html')
def password_reset_post():
    viewmodel = PasswordResetRequestViewModel()
    viewmodel.validate()

    if viewmodel.error:
        return viewmodel.to_dict()

    viewmodel.user = user_service.find_user_by_email(viewmodel.email)
    if viewmodel.user:
        user_token = generate_token(viewmodel.user.uuid)
        viewmodel.confirm_url = url_for('account.verified_password_reset_get', token=user_token, _external=True)
        html = render_template('account/password_reset_email_contents.html', confirm_url=viewmodel.confirm_url)
        email_subject = 'Password Reset'
        send_email(viewmodel.email, email_subject, html)

        # log details of the password reset request
        current_app.logger.info(f'Password reset requested for user: {viewmodel.user.uuid}')

        # flash success message
        flash('Password reset email sent. Please check your email.')
        return redirect('/account/login')
    else:
        viewmodel.error = 'No account with that email exists.'
        return viewmodel.to_dict()


# ################### PASSWORD CHANGE ###################################


@blueprint.route('/account/change_password', methods=['GET'])
@response(template_file='account/change_password.html')
def change_password_get():
    viewmodel = ViewModelBase()

    if viewmodel.user_id is None:
        flash('You must be logged in to change your password.')
        return redirect('/account/login')

    return viewmodel.to_dict()


@blueprint.route('/account/change_password', methods=['POST'])
@response(template_file='account/change_password.html')
def change_password_post():
    viewmodel = PwUpdateViewModel()
    viewmodel.validate()

    # check for errors in the form
    if viewmodel.error:
        return viewmodel.to_dict()

    # update the user's password
    password_change = user_service.update_password(viewmodel.user_id, viewmodel.new_password)
    if not password_change[0]:
        viewmodel.error = password_change[1]
        return viewmodel.to_dict()

    flash('You have successfully changed your password')
    return redirect('/account')


# ################### EMAIL CHANGE ###################################


@blueprint.route('/account/change_email', methods=['GET'])
@response(template_file='account/change_email.html')
def change_email_get():
    viewmodel = ViewModelBase()

    if viewmodel.user_id is None:
        flash('You must be logged in to change your email.')
        return redirect('/account/login')

    return viewmodel.to_dict()


@blueprint.route('/account/change_email', methods=['POST'])
@response(template_file='account/change_email.html')
def change_email_post():
    viewmodel = EmailUpdateViewModel()
    viewmodel.validate()

    if viewmodel.user_id is None:
        flash('You must be logged in to change your email.')
        return redirect('/account/login')

    if viewmodel.error:
        return viewmodel.to_dict()

    # update the user's email
    email_change = user_service.update_email(viewmodel.user_id, viewmodel.new_email)
    if email_change:
        service = user_service.update_email_confirmation(viewmodel.new_email)
        if service:
            email_token = generate_token(viewmodel.new_email)
            viewmodel.confirm_url = url_for('account.confirm_email', token=email_token, _external=True)
            html = render_template('account/activate_account_email_contents.html', confirm_url=viewmodel.confirm_url)
            email_subject = 'Please Confirm Email'
            send_email(viewmodel.new_email, email_subject, html)
            return redirect('/unconfirmed')
    return viewmodel.to_dict()
