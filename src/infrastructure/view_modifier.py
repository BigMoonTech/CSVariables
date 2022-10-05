from functools import wraps

import flask
import werkzeug
import werkzeug.wrappers


def response(*, mimetype: str = None, template_file: str = None):
    """Decorator to wrap a view function and force it to return a response object."""

    def response_inner(f):

        @wraps(f)
        def view_method(*args, **kwargs):
            # Call the view function and get the response value
            response_val = f(*args, **kwargs)

            # If the response is already a response object, return it
            if isinstance(response_val, werkzeug.wrappers.Response):
                return response_val

            # If the response is a flask response object, return it
            if isinstance(response_val, flask.Response):
                return response_val

            # If the response is a dict, create a model from it
            if isinstance(response_val, dict):
                model = dict(response_val)
            else:
                model = dict()

            # If response_val is not a dict, raise an exception
            if template_file and not isinstance(response_val, dict):
                raise Exception(
                    "Invalid return type {}, we expected a dict as the return value.".format(type(response_val)))

            # sets up what template to render, and unpacks the variables, args, etc. to be passed into the template
            if template_file:
                response_val = flask.render_template(template_file, **response_val)

            # useful for forcing the return value of a view method to a response (for the decorator)
            resp = flask.make_response(response_val)
            resp.model = model
            if mimetype:
                resp.mimetype = mimetype

            return resp

        return view_method

    return response_inner
