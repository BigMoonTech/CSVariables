"""Main app module."""

import os
import sys

from flask import Flask

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

app = Flask(__name__)


def main():
    """Run the Flask app."""
    configure()
    app.run(debug=True, port=5006)


def configure():
    """Configure Flask app."""
    print("Configuring Flask app:")

    register_blueprints()
    print("Registered blueprints")

    # setup_db()
    # print("DB setup completed.")
    print("", flush=True)


def register_blueprints():
    """Register Flask blueprints."""
    from src.views import home_views
    app.register_blueprint(home_views.blueprint)


if __name__ == '__main__':
    main()
else:
    configure()
