import numpy as np
from sklearn import svm

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

        raise NotImplementedError(
            "Method %s#train not implemented." % self.__class__.__name__)

    def predict(self, document):
        """Predicts label for given document.
        Note that before running this method, method ``train`` must be run.

        :param document: Document to be labeled.
        :returns: Predicted label of the document.
        """

        raise NotImplementedError(
            "Method %s#predict not implemented." % self.__class__.__name__)


class NaiveBayesModel(AbstractModel):
    """Naive Bayes model. No +1 smoothing is used in this model, the selector
    is expected to remove words that are not in the vocabulary.
    """

    def __init__(self, feature_selector):
        super(NaiveBayesModel, self).__init__(feature_selector)

    def train(self, documents):
        X, Y = self.feature_selector.build(documents)
        P_Y = np.bincount(np.concatenate(Y))
        P_Y = P_Y/float(P_Y.size)
        P_XY = []
        for i in range(P_Y.size):
            P_XY_i = np.sum(X * (Y == i), axis=0) / P_Y[i]
            P_XY.append(P_XY_i)

        self.prior = np.transpose([P_Y])
        self.likelihood = np.array(P_XY)

    def predict(self, document):
        x = self.feature_selector.get_x(document)
        predictions = self.prior * np.transpose(
            [np.product(self.likelihood ** x, axis=1)])
        y = np.argmax(predictions)
        label = self.feature_selector.get_label(y)

        return label


class SVMModel(AbstractModel):
    """Support Vector Machine model."""

    def __init__(self, feature_selector, kernel=GaussianKernel(), C=1):
        super(SVMModel, self).__init__(feature_selector)
        self.C = C
        self.kernel = kernel

    def train(self, documents):
        X, Y = self.feature_selector.build(documents)
        if hasattr(self.kernel, 'sklearn_name'):
            self.svm = svm.SVC(C=self.C, kernel=self.kernel.sklearn_name,
                               **self.kernel.sklearn_params)
        else:
            self.svm = svm.SVC(C=self.C, kernel=self.kernel.compute)
        self.svm.fit(X, np.concatenate(Y))

    def predict(self, document):
        x = self.feature_selector.get_x(document)
        y = self.svm.predict([x])
        label = self.feature_selector.get_label(y)

        return label
