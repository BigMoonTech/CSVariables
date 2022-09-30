from flask import Blueprint, redirect
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

    if viewmodel.error is None:
        resp = cs.call_openai(viewmodel.prompt)

        # todo: (todo is in the completion service) handle a no response error from openai

        viewmodel.resp_text = cs.get_choices_text(resp)

        cs.add_completion_to_db(resp, viewmodel.prompt, viewmodel.ip_address)

        # Update unregistered user table
        if us.update_unregistered_user_calls(viewmodel.ip_address) is None:
            viewmodel.error = 'There was an error updating your unregistered user data.'
            # todo: log this type of error
    else:
        viewmodel.resp_text = viewmodel.error

    return viewmodel.to_dict()


@blueprint.route('/about')
@response(template_file='home/about.html')
def about():
    # we can just use the base viewmodel here to pass the user_id to the template
    viewmodel = ViewModelBase()
    return viewmodel.to_dict()
