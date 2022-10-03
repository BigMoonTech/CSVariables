from flask import Blueprint, redirect, flash, current_app
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

    if viewmodel.user_id is None:
        flash('Please login to access the application.')
        return redirect('/account/login')

    viewmodel.prompt = viewmodel.request_dict.query.strip()
    viewmodel.validate()

    if viewmodel.error:
        viewmodel.resp_text = viewmodel.error

    else:

        resp = cs.validated_openai_response(viewmodel.prompt)

        if not isinstance(resp, dict):
            viewmodel.error = resp
        else:
            viewmodel.resp_text = cs.get_choices_text(resp)

            # record the completion in the database
            if not cs.add_completion_to_db(resp, viewmodel.prompt, viewmodel.ip_address, viewmodel.user_id):
                current_app.logger.error('Failed to add completion to the database.')
                viewmodel.error = 'There was an error saving your completion. Please try again.'

            # Update registered user table
            elif us.update_registered_user_calls(viewmodel.user_id) is None:
                # if this happens, it's a big deal, (infinite calls is bad mmkay) so I'm logging it
                current_app.logger.error("There was an error updating the user's remaining calls.")
                viewmodel.error = 'There was an error updating your remaining calls. Please contact support.'

    return viewmodel.to_dict()
