from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from redis import Redis
from rq import Queue

app = Flask(__name__)
app.config.from_object("triager.settings")
db = SQLAlchemy(app)
q = Queue(connection=Redis())

import views  # noqa
import models  # noqa
import filters  # noqa

# Create database
db.create_all()
