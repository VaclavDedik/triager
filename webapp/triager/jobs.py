import os
import time
import joblib
import random
import numpy as np

from classifier import models, selectors, kernels, utils, tests

from triager import db, app
from models import Project, TrainStatus


def train_project(id):
    try:
        project = Project.query.get(id)

        # retrieve data
        # TODO: add to configuration
        data = project.datasource.get_data()[-3000:]
        data = utils.filter_docs(data, min_class_occur=30)

        # create training model
        print("Training model for project %s" % id)
        selector = selectors.TFIDFDecorator(selectors.StopWordsDecorator(
            selectors.BasicSelector()))
        kernel = kernels.GaussianKernel()
        model = models.SVMModel(
            feature_selector=selector, kernel=kernel, C=240, cache_size=2000)

        # train model
        model.train(data)
        print("Model for project %s successfully trained" % id)

        # create testing model
        print("Training model for project %s for testing" % id)
        selector_test = selectors.TFIDFDecorator(selectors.StopWordsDecorator(
            selectors.BasicSelector()))
        kernel_test = kernels.GaussianKernel()
        model_test = models.SVMModel(
            feature_selector=selector_test, kernel=kernel_test,
            C=240, cache_size=2000)

        # split data for testing
        random.shuffle(data)
        n = len(data)
        split_pct = 8/10.0
        split_x = int(np.ceil(n*split_pct))
        data_train = data[:split_x]
        data_test = data[split_x:]

        # train testing model
        model_test.train(data_train)
        print("Testing model for project %s successfully trained" % id)

        # testing model
        project.accuracy = tests.accuracy(model_test, data_test)
        project.precision, project.recall = tests.precision_and_recall(
            model_test, data_test)

        # save
        dump_dir = os.path.join(app.config['MODEL_FOLDER'], str(id))
        if not os.path.exists(dump_dir):
            os.mkdir(dump_dir)
        joblib.dump(model, os.path.join(dump_dir, 'svm.pkl'))
        project.train_status = TrainStatus.TRAINED
        project.last_training = time.time()
        db.session.add(project)
        db.session.commit()
    except Exception as ex:
        project.train_status = TrainStatus.FAILED
        project.training_message = "Reason: %s" % ex
        db.session.add(project)
        db.session.commit()
        raise ex
