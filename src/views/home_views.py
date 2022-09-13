from flask import Blueprint, request
from src.infrastructure.view_modifier import response
from src.view_models.home.home_viewmodel import HomeViewModel
from src.services import completion_service as cs
from src.services import user_service as us


blueprint = Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/', methods=['GET', 'POST'])
@response(template_file='home/index.html')
def index():
    """Handle requests for the application home page."""
    viewmodel = HomeViewModel()

    if request.method == 'POST' and viewmodel.validate():
        # todo: move this to the viewmodel
        prompt = viewmodel.request_dict.query

        viewmodel.error = cs.validate_prompt_len(prompt)

        if viewmodel.error is None:
            resp = cs.call_openai(prompt)

            # todo: (todo is in the completion service) handle a no response error from openai

            resp_text = cs.get_choices_text(resp)

            viewmodel.resp_text = resp_text

            cs.add_completion_to_db(resp, prompt, viewmodel.ip_address, viewmodel.user_id)

            # Update unregistered user table if the user is not logged in
            if not viewmodel.user_id:
                if us.update_unregistered_user_calls(viewmodel.ip_address) is None:

                    viewmodel.error = 'There was an error updating your unregistered user data.'
                    # todo: log this type of error
            else:
                if us.update_registered_user_calls(viewmodel.user_id) is None:

                    viewmodel.error = 'There was an error updating your remaining calls.'
                    # todo: log this type of error

        else:
            viewmodel.resp_text = viewmodel.error

    return viewmodel.to_dict()


@blueprint.route('/about')
@response(template_file='home/about.html')
def about():
    return {}
