from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from redis import Redis
from rq import Queue
from rq.job import JobStatus

app = Flask(__name__)
app.config.from_object("triager.settings")
db = SQLAlchemy(app)
q = Queue(connection=Redis())

import views  # noqa
import models  # noqa
import filters  # noqa
import jobs

# Create database
db.create_all()

# Run loop that checks for scheduled jobs
scheduler = q.fetch_job("retrain_scheduled_loop")
if not scheduler or scheduler.status == JobStatus.FAILED:
    q.enqueue(jobs.retrain_scheduled_loop, job_id="retrain_scheduled_loop",
              timeout=2147483647)
