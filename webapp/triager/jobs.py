import os
import joblib

from classifier import models, selectors, kernels, utils

from triager import db, app
from models import Project, TrainStatus


def train_project(id):
    try:
        project = Project.query.get(id)

        # retrieve data
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

        # save
        dump_dir = os.path.join(app.config['MODEL_FOLDER'], str(id))
        if not os.path.exists(dump_dir):
            os.mkdir(dump_dir)
        joblib.dump(model, os.path.join(dump_dir, 'svm.pkl'))
        project.train_status = TrainStatus.TRAINED
        db.session.add(project)
        db.session.commit()
    except Exception as ex:
        project.train_status = TrainStatus.FAILED
        db.session.add(project)
        db.session.commit()
        raise ex
