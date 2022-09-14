"""Main app module."""
import logging
import os
import sys
import flask
import openai

from flask import Flask

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from src.db_models import db_session

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)


def main():
    """Run the Flask app."""
    configure()
    app.run(debug=True, port=5006)


def configure():
    """Configure Flask app."""
    print("Configuring Flask app:")

    # Configure OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        app.logger.critical('OpenAi API key was not Found')
        return flask.abort(404)
    print("Configured OpenAI API key.")

    # Configure Blueprints
    register_blueprints()
    print("Registered blueprints")

    setup_db()
    print("DB setup completed.")
    print("", flush=True)


def setup_db():
    """Setup DB."""
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'csve.sqlite')

    db_session.global_init(db_file)


def register_blueprints():
    """Register Flask blueprints."""
    app.logger.info('Registering Blueprints')
    from src.views import home_views
    from src.views import account_views
    from src.views import app_views

    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(app_views.blueprint)
    app.logger.info('Blueprints Registered')


if __name__ == '__main__':
    main()
else:
    configure()
