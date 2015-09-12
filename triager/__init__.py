from configuration import Configuration

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask import Flask

app = Flask(__name__)
app.config.from_object("triager.settings")
app.config.from_envvar("TRIAGER_SETTINGS", silent=True)
db = SQLAlchemy(app)
login_manager = LoginManager()
config = Configuration(app.config['STORAGE_FOLDER'])

import views  # noqa
import models  # noqa
import filters  # noqa
import auth  # noqa

# Create database
db.create_all()

# Init login
login_manager.init_app(app)
