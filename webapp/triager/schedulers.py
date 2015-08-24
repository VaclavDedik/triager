import time
import signal

from multiprocessing import Pool
from flask.ext.script import Command

from croniter import croniter
from triager import db, jobs
from models import Project, TrainStatus


class RetrainScheduler(Command):

    def _train_project(self, project_id):
        try:
            jobs.train_project(project_id)
        except KeyboardInterrupt:
            pass

    def _retrain_loop(self, pool):
        while True:
            projects = Project.query

            print("Found %s projects" % projects.count())
            for project in projects:
                print("Checking if project %s needs training" % project.id)
                if project.train_status != TrainStatus.TRAINING:
                    print ("Project %s is not training" % project.id)
                    crontab = croniter(project.schedule, project.last_training)
                    nextrun = crontab.get_next()

                    if nextrun <= time.time():
                        print("Queuing scheduled project %s for training"
                              % project.id)
                        project.train_status = TrainStatus.TRAINING
                        db.session.add(project)
                        db.session.commit()

                        pool.apply_async(self._train_project, (project.id,))

            time.sleep(60)

    def _sigint_handler(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def run(self):
        pool = Pool(processes=5, initializer=self._sigint_handler)

        try:
            self._retrain_loop(pool)
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
