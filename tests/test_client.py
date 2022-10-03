# noinspection PyPackageRequirements
import pytest
import sys
import os

from src.db_models import db_session

container_folder = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'
))
sys.path.insert(0, container_folder)

from src import app as flask_app


@pytest.fixture
def client():
    # set the config to the TestingConfig instead of the DevelopmentConfig
    flask_app.config.from_object("src.config.TestingConfig")

    db_file = flask_app.config.get('SQLALCHEMY_DATABASE_URI')
    db_session.global_init(db_file)  # we must initialize the db_session with the correct uri
    print("DB setup completed.")

    # __init__ is executed when src is referenced in the import above
    # so blueprints are already created, and openai key set
    print('OpenAI key set already')
    print('Blueprints are already created')

    client = flask_app.test_client()
    yield client
