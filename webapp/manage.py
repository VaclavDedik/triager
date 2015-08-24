from flask.ext.script import Manager, Server

from triager import app
from triager.schedulers import RetrainScheduler


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('runscheduler', RetrainScheduler())


if __name__ == '__main__':
    manager.run()
