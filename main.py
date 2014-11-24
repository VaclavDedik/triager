#!/usr/bin/env python

from triager.classifier import models, kernels, selectors, tests
from triager import parsers


def main():
    # Parse MRS data into documents
    parser = parsers.MRSParser("data/unify/MRs/")
    print "Parsing data from %s..." % parser.folder
    documents = parser.parse()
    # Filter unlabeled documents
    documents = [doc for doc in documents if doc.label]
    # Split between train and cv data
    docs_train = documents[:1500]
    docs_cv = documents[1500:]
    # Create model
    selector = selectors.StopWordsDecorator(selectors.BasicSelector())
    kernel = kernels.GaussianKernel()
    model = models.SVMModel(feature_selector=selector, kernel=kernel, C=35)
    print "Created model %s, using feature selector %s." \
        % (model.__class__.__name__, model.feature_selector.__class__.__name__)
    # Train model
    print "Training model..."
    model.train(docs_train)
    # Test model
    print "Computing accuracy for train set..."
    accuracy_train = tests.accuracy(model, docs_train)
    print "Computing accuracy for CV set..."
    accuracy_cv = tests.accuracy(model, docs_cv)

    print "Accuracy of train set is: '%.4f'." % accuracy_train
    print "Accuracy of CV set is: '%.4f'." % accuracy_cv

if __name__ == "__main__":
    main()
