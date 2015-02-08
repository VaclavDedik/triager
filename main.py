#!/usr/bin/env python

import numpy as np

from triager.classifier import models, kernels, selectors, tests, utils
from triager import parsers


def main():
    # Parse data into documents
    parser = parsers.MRSParser("data/unify/MRs/", project_match="OPW.*")
    #parser = parsers.BugzillaParser("data/opensource/mozilla_firefox")
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

    # Test model (accuracy)
    print "Computing accuracy for train set (size=%s)..." % len(docs_train)
    accuracy_train = tests.accuracy(model, docs_train)
    print "Computing accuracy for CV set (size=%s)..." % len(docs_cv)
    accuracy_cv = tests.accuracy(model, docs_cv)
    print "Accuracy of train set is: '%.4f'." % accuracy_train
    print "Accuracy of CV set is: '%.4f'." % accuracy_cv
    # Test model (precision and recall)
    print "Computing average precision and recall for train set..."
    pr_train = tests.precision_and_recall(model, docs_train)
    print "Computing average precision and recall for CV set..."
    pr_cv = tests.precision_and_recall(model, docs_cv)
    print "Average precision and recall of train set is: '%.4f' and '%.4f'." \
        % pr_train
    print "Average precision and recall of CV set is: '%.4f' and '%.4f'." \
        % pr_cv

if __name__ == "__main__":
    main()
