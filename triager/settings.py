import os
import logging

#: Debug flag.
DEBUG = True

#: Folders where to store data.
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER = os.path.join(APP_ROOT, '../data')
MODEL_FOLDER = os.path.join(STORAGE_FOLDER, 'model')

#: Important files
SCHEDULER_PID_FILE = os.path.join(STORAGE_FOLDER, 'scheduler.pid')

#: Logging level.
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

#: Logging format.
LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'

#: Logging directory.
LOG_DIR = os.path.join(APP_ROOT, '../logs')

#: Whether to log connecting to database or not.
LOG_DB_CONNECTIONS = False

#: SQLAlchemy configuration.
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/triager.db' % STORAGE_FOLDER
SQLALCHEMY_ECHO = False

#: WTForms CSRF protection
CSRF_ENABLED = True
SECRET_KEY = 'secret'

# Create storage, model and log directories if they do not exist.
if not os.path.exists(STORAGE_FOLDER):
    os.makedirs(STORAGE_FOLDER)
if not os.path.exists(MODEL_FOLDER):
    os.makedirs(MODEL_FOLDER)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
