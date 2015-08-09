import logging

#: Debug flag.
DEBUG = True

#: Logging level.
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

#: Logging format.
LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'

#: Whether to log connecting to database or not.
LOG_DB_CONNECTIONS = False

#: SQLAlchemy connection.
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/triager.db'

#: WTForms CSRF protection
CSRF_ENABLED = True
SECRET_KEY = 'secret'
