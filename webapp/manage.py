import os
import sys
import logging

from flask.ext.script import Manager, Server

from triager import app
from triager.schedulers import RetrainScheduler


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('runscheduler', RetrainScheduler())

if __name__ == '__main__':
    # Setup logging
    log_file = 'app.log'
    if 'runscheduler' in sys.argv:
        log_file = 'scheduler.log'
    logging.basicConfig(
        format=app.config['LOG_FORMAT'], level=app.config['LOG_LEVEL'],
        filename=os.path.join(app.config['LOG_DIR'], log_file)
    )

    manager.run()
