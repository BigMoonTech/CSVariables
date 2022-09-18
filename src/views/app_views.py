from flask import Blueprint, redirect
from src.infrastructure.view_modifier import response
from src.view_models.home.app_viewmodel import AppViewModel
from src.services import completion_service as cs
from src.services import user_service as us

blueprint = Blueprint('app', __name__, template_folder='templates')


@blueprint.route('/app', methods=['GET'])
@response(template_file='home/app.html')
def app_get():
    """Handle requests for the application main page."""
    viewmodel = AppViewModel()

    if viewmodel.user_id is None:
        return redirect('/account/login')

    elif not viewmodel.user.confirmed:
        return redirect('/unconfirmed')

    return viewmodel.to_dict()


@blueprint.route('/app', methods=['POST'])
@response(template_file='home/app.html')
def app_post():
    """Handle requests for the application page."""
    viewmodel = AppViewModel()
    viewmodel.prompt = viewmodel.request_dict.query.strip()

    viewmodel.validate()

    if viewmodel.error is None:

        resp = cs.call_openai(viewmodel.prompt)

        # todo: (handle a no response error from openai, or a bad response)

        viewmodel.resp_text = cs.get_choices_text(resp)

        cs.add_completion_to_db(resp, viewmodel.prompt, viewmodel.ip_address, viewmodel.user_id)

        # Update registered user table
        if us.update_registered_user_calls(viewmodel.user_id) is None:
            viewmodel.error = 'There was an error updating your remaining calls.'
            # todo: log this type of error

    else:
        viewmodel.resp_text = viewmodel.error

    return viewmodel.to_dict()
