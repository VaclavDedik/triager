import os
import logging

#: Debug flag.
DEBUG = True

#: Folders where to store data.
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER = os.path.join(APP_ROOT, '../data')
MODEL_FOLDER = os.path.join(STORAGE_FOLDER, 'model')

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
