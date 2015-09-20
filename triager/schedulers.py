import os
import time
import signal
import logging

from datetime import datetime
from multiprocessing import Pool
from flask.ext.script import Command

from croniter import croniter
from triager import jobs, db, app
from models import Project, TrainStatus as TS


class RetrainScheduler(Command):
    DAY = 60*60*24

    def _train_project(self, project):
        logging.info("Queuing scheduled project %s for training" % project.id)

        project.train_status = TS.QUEUED
        db.session.add(project)
        db.session.commit()

        self.pool.apply_async(jobs.train_project, (project.id,))

    def _retrain_loop(self):
        while True:
            projects = Project.query

            logging.debug("Found %s projects" % projects.count())
            for project in projects:
                logging.debug("Checking if project %s needs training"
                              % project.id)

                crontab = croniter(project.schedule, project.last_training)
                nextrun = crontab.get_next()
                status = project.train_status

                p_format = '%Y-%m-%d %H:%M:%S'
                p_last_training = datetime.fromtimestamp(
                    project.last_training).strftime(p_format)
                p_nextrun = datetime.fromtimestamp(
                    nextrun).strftime(p_format)

                logging.debug("Project %s last build %s, next build %s"
                              % (project.id, p_last_training, p_nextrun))

                if nextrun <= time.time():
                    if not TS.is_active(status):
                        logging.info("Project %s is not in an active status"
                                     % project.id)
                        self._train_project(project)
                    elif status == TS.FAILED and \
                            nextrun + self.DAY <= time.time():
                        logging.warning(
                            "Project %s failed a day ago, trying again"
                            % project.id)
                        self._train_project(project)

            db.session.expire_all()
            time.sleep(60)

    def _pool_init(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def run(self):
        # Save scheduler.pid in data directory
        with open(app.config['SCHEDULER_PID_FILE'], 'w') as f:
            f.write(str(os.getpid()))

        # Check projects that are in QUEUED and TRAINING statues and move
        # them to FAILED
        projects = Project.query
        for project in projects:
            if project.train_status in [TS.QUEUED, TS.TRAINING]:
                logging.warning("Project %s in state '%s' on scheduler startup"
                                % (project.id, project.train_status))
                project.train_status = TS.FAILED
                project.training_message = \
                    "Reason: Scheduler stopped unexpectedly"
                db.session.add(project)
        else:
            db.session.commit()

        # Create new pool
        self.pool = Pool(processes=app.config['SCHEDULER_PROCESSES'],
                         initializer=self._pool_init)

        # Start infinite loop
        try:
            self._retrain_loop()
        except KeyboardInterrupt:
            logging.warning(
                "Keybord interrupt detected, terminating scheduler.")
            self.pool.terminate()
            self.pool.join()
