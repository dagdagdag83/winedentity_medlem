import os
import logging
from flask import Flask
from .db import Database
from .mock_db import MockDatabase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SESSION_SECRET_KEY', 'a_hard_to_guess_string')
app.config['RECAPTCHA_SITE_KEY'] = os.environ.get('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = os.environ.get('RECAPTCHA_SECRET_KEY')

# Initialize Database
# Use mock database if ENV is set to 'local'
if os.environ.get('ENV') == 'local':
    db_manager = MockDatabase()
    logging.info("Using Mock Database for local development.")
else:
    db_manager = Database()
    logging.info("Using Google Cloud Datastore.")

# Import the routes to register them with the app
# This import is at the end to avoid circular dependencies
from . import main
