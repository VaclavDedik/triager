#!/usr/bin/env python

import numpy as np

from triager.classifier import models, kernels, selectors, tests, utils
from triager import parsers


def main():
    # Parse MRS data into documents
    parser = parsers.MRSParser("data/unify/MRs/")
    print "Parsing data from %s..." % parser.folder
    documents = parser.parse()
    # Filter unlabeled documents and documents that are not labeled with
    # a class that occurs at lest `min_class_occur`
    documents = [doc for doc in documents if doc.label]
    documents = utils.filter_docs(documents, min_class_occur=30)
    # Split between train and cv data
    n = len(documents)
    split_pct = 7/10.0
    split_x = int(np.ceil(n*split_pct))
    docs_train = documents[:split_x]
    docs_cv = documents[split_x:]
    # Create model
    selector = selectors.TFIDFDecorator(selectors.StopWordsDecorator(
        selectors.BasicSelector()))
    kernel = kernels.GaussianKernel()
    model = models.SVMModel(feature_selector=selector, kernel=kernel, C=240)
    print "Created model %s, using feature selector %s." \
        % (model.__class__.__name__, model.feature_selector.__class__.__name__)
    # Train model
    print "Training model on %s instances..." % len(docs_train)
    model.train(docs_train)
    print "Number of classes is: %s" % len(model.feature_selector.labels)
    # Test model
    print "Computing accuracy for train set (size=%s)..." % len(docs_train)
    accuracy_train = tests.accuracy(model, docs_train)
    print "Computing accuracy for CV set (size=%s)..." % len(docs_cv)
    accuracy_cv = tests.accuracy(model, docs_cv)

    print "Accuracy of train set is: '%.4f'." % accuracy_train
    print "Accuracy of CV set is: '%.4f'." % accuracy_cv

if __name__ == "__main__":
    main()
