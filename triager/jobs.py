import os
import time
import joblib
import random
import logging
import numpy as np

from classifier import models, selectors, kernels, utils, tests

from triager import db, app, config
from models import Project, TrainStatus as TS


def train_project(id):
    try:
        logging.info("Started training project %s" % id)
        project = Project.query.get(id)
        project.train_status = TS.TRAINING
        db.session.add(project)
        db.session.commit()

        # Config
        config.reload()
        ticket_limit = int(config.general__ticket_limit)
        min_class_occur = int(config.general__min_class_occur)
        C = float(config.svm__coefficient)
        cache_size = int(config.svm__cache_size)

        # retrieve data
        # TODO: add to configuration
        data = project.datasource.get_data()[-ticket_limit:]
        data = utils.filter_docs(data, min_class_occur=min_class_occur)

        # create training model
        logging.debug("Training model for project %s" % id)
        selector = selectors.TFIDFDecorator(selectors.StopWordsDecorator(
            selectors.BasicSelector()))
        kernel = kernels.GaussianKernel()
        model = models.SVMModel(
            feature_selector=selector, kernel=kernel,
            C=C, cache_size=cache_size)

        # train model
        model.train(data)
        logging.debug("Model for project %s successfully trained" % id)

        # create testing model
        logging.debug("Training model for project %s for testing" % id)
        selector_test = selectors.TFIDFDecorator(selectors.StopWordsDecorator(
            selectors.BasicSelector()))
        kernel_test = kernels.GaussianKernel()
        model_test = models.SVMModel(
            feature_selector=selector_test, kernel=kernel_test,
            C=C, cache_size=cache_size)

        # split data for testing
        random.shuffle(data)
        n = len(data)
        split_pct = 8/10.0
        split_x = int(np.ceil(n*split_pct))
        data_train = data[:split_x]
        data_test = data[split_x:]

        # train testing model
        model_test.train(data_train)
        logging.debug("Testing model for project %s successfully trained" % id)

        # testing model
        project.accuracy = tests.accuracy(model_test, data_test)
        project.precision, project.recall = tests.precision_and_recall(
            model_test, data_test)

        # save
        dump_dir = os.path.join(app.config['MODEL_FOLDER'], str(id))
        if not os.path.exists(dump_dir):
            os.mkdir(dump_dir)
        joblib.dump(model, os.path.join(dump_dir, 'svm.pkl'))
        project.train_status = TS.TRAINED
        project.last_training = time.time()
        db.session.add(project)
        db.session.commit()
        logging.info("Project %s successfully trained and updated." % id)
    except Exception as ex:
        logging.error("Failed to train project %s" % id)
        logging.exception(ex)

        project.train_status = TS.FAILED
        project.training_message = "Reason: %s" % ex
        db.session.add(project)
        db.session.commit()
