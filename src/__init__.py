"""Main app initialization."""

import logging
import os
import sys
import openai
from flask import Flask

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from src.db_models import db_session
from src.db_models.db_session import __factory

# configure logging
logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)

# configure the app
print("Configuring Flask app:")
app.config.from_object(os.environ['APP_SETTINGS'])

# Configure OpenAI
openai.api_key = app.config.get('OPENAI_API_KEY')
if not openai.api_key:
    app.logger.critical('OpenAi API key was not Found')
print("Configured OpenAI API key.")

db_file = app.config.get('SQLALCHEMY_DATABASE_URI')

# If the following block of code was in db_session.global_init
# then it prevents some db integration tests from working.
# (src.app would still be referencing the development version
# of the db uri, [the SQLALCHEMY_DATABASE_URI variable])
if not __factory:
    db_session.global_init(db_file)  # initialize the db_session with the correct uri
    print("DB setup completed.")

print("", flush=True)

# Configure Blueprints
print("Registering blueprints...")
app.logger.info('Registering Blueprints...')
from src.views import home_views
from src.views import account_views
from src.views import app_views
app.register_blueprint(account_views.blueprint)
app.register_blueprint(home_views.blueprint)
app.register_blueprint(app_views.blueprint)
print("Registered blueprints.")
app.logger.info('Blueprints Registered')

print("Flask app configured.")
