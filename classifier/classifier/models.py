import numpy as np
import operator
from sklearn import naive_bayes
from sklearn import svm, tree

from kernels import GaussianKernel


class AbstractModel(object):
    """Abstract model of a learning algorithm. When implementing a subclass,
    you have to implement method ``train``. Method ``predict`` is implemented
    by default.
    """

    def __init__(self, feature_selector):
        """Default initializer requires only feature selector to be specified.
        If you want to add additional parameters to your implementation of the
        model, be sure to call this initializer in your initializer first.

        :param feature_selector: Feature selector class from package
               ``selectors``.
        """

        self.feature_selector = feature_selector

    def train(self, documents):
        """Trains the model on the provided list of **labeled** documents.
        This method is expected to initialize some sort of predictor field(s)
        that will be used by method ``predict``, e.g. in Naive Bayes model,
        the initialized fields could be ``prior`` and ``likelihood``.

        :param documents: Labeled documents used to train the predictor.
        """

        raise NotImplementedError()

    def predict(self, document, n=1):
        """Predicts label(s) for given document.
        Note that before running this method, method ``train`` must be run.

        :param document: Document to be labeled.
        :param n: Number of predictions, 1 by default.
        :returns: Predicted label(s) of the document in descending order.
        """

        raise NotImplementedError()


class BaselineModel(AbstractModel):
    """This baseline model always predict label that is the most frequent."""

    def __init__(self, feature_selector):
        super(BaselineModel, self).__init__(feature_selector)

    def train(self, documents):
        X, Y = self.feature_selector.build(documents)
        labels_freq = {}
        for document in documents:
            if document.label in labels_freq:
                labels_freq[document.label] += 1
            else:
                labels_freq[document.label] = 1

        self.labels_freq = sorted(labels_freq.items(), reverse=True,
                                  key=operator.itemgetter(1))

    def predict(self, document, n=1):
        top_n = self.labels_freq[:n]
        labels = map(lambda x: x[0], top_n)
        return labels


class NaiveBayesModel(AbstractModel):
    """Naive Bayes model. No +1 smoothing is used in this model, the selector
    is expected to remove words that are not in the vocabulary.
    """

    def __init__(self, feature_selector):
        super(NaiveBayesModel, self).__init__(feature_selector)

    def train(self, documents):
        X, Y = self.feature_selector.build(documents)
        nb = naive_bayes.GaussianNB()
        nb.fit(X, np.concatenate(Y))
        self.nb = nb

    def predict(self, document, n=1):
        x = self.feature_selector.get_x(document)
        probs = self.nb.predict_proba([x])[0]
        Y = probs.argsort()[::-1]
        labels = map(self.feature_selector.get_label, Y)

        return labels[:n]

    def __str__(self):
        return "NaiveBayesModel(feature_selector=%s)" \
            % self.feature_selector


class SVMModel(AbstractModel):
    """Support Vector Machine model."""

    def __init__(self, feature_selector, kernel=GaussianKernel(), C=1,
                 cache_size=200):
        super(SVMModel, self).__init__(feature_selector)
        self.C = C
        self.kernel = kernel
        self.cache_size = cache_size

    def train(self, documents):
        X, Y = self.feature_selector.build(documents)
        if hasattr(self.kernel, 'sklearn_name'):
            self.svm = svm.SVC(C=self.C, kernel=self.kernel.sklearn_name,
                               probability=True, cache_size=self.cache_size,
                               **self.kernel.sklearn_params)
        else:
            self.svm = svm.SVC(C=self.C, kernel=self.kernel.compute)
        self.svm.fit(X, np.concatenate(Y))

    def predict(self, document, n=1):
        x = self.feature_selector.get_x(document)
        probs = self.svm.predict_proba([x])[0]
        Y = probs.argsort()[::-1]
        labels = map(self.feature_selector.get_label, Y)

        return labels[:n]

    def __str__(self):
        return "SVMModel(feature_selector=%s, kernel=%s, C=%s)" \
            % (self.feature_selector, self.kernel, self.C)


class CARTModel(AbstractModel):
    "Decision Tree Model using CART algorithm."

    def __init__(self, feature_selector):
        super(CARTModel, self).__init__(feature_selector)

    def train(self, documents):
        X, Y = self.feature_selector.build(documents)
        self.clf = tree.DecisionTreeClassifier()
        self.clf.fit(X, np.concatenate(Y))

    def predict(self, document, n=1):
        x = self.feature_selector.get_x(document)
        probs = self.clf.predict_proba([x])[0]
        Y = probs.argsort()[::-1]
        labels = map(self.feature_selector.get_label, Y)

        return labels[:n]

    def __str__(self):
        return "CARTModel(feature_selector=%s)" % self.feature_selector
