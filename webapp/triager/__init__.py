from configuration import Configuration

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.from_object("triager.settings")
db = SQLAlchemy(app)
config = Configuration(app.config['STORAGE_FOLDER'])

import views  # noqa
import models  # noqa
import filters  # noqa

# Create database
db.create_all()
