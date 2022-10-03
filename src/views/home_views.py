from flask import Blueprint, redirect, current_app
from src.infrastructure.view_modifier import response
from src.view_models.home.home_viewmodel import HomeViewModel
from src.services import completion_service as cs
from src.services import user_service as us
from src.view_models.shared.viewmodel_base import ViewModelBase

blueprint = Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/', methods=['GET'])
@response(template_file='home/index.html')
def index_get():
    viewmodel = HomeViewModel()

    if viewmodel.user_id is not None:
        return redirect('/app')

    return viewmodel.to_dict()


@blueprint.route('/', methods=['POST'])
@response(template_file='home/index.html')
def index_post():
    """Handle requests for the application home page."""
    viewmodel = HomeViewModel()
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

            if not cs.add_completion_to_db(resp, viewmodel.prompt, viewmodel.ip_address):
                current_app.logger.error('Failed to add an unregistered user completion to the database.')
                # I want the user to still see their query results, so I'm not setting viewmodel.error here.

            # Update unregistered user table
            elif us.update_unregistered_user_calls(viewmodel.ip_address) is None:
                # if this happens, it's a big deal, so I'm logging it
                current_app.logger.error("There was an error updating the unregistered user's remaining calls.")
                viewmodel.error = 'There was an error updating your unregistered user data. Please create an account ' \
                                  'to view your saved your completions.'

    return viewmodel.to_dict()


@blueprint.route('/about')
@response(template_file='home/about.html')
def about():
    # we can just use the base viewmodel here to pass the user_id to the template
    viewmodel = ViewModelBase()
    return viewmodel.to_dict()
