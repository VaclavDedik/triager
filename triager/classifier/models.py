import numpy as np


class AbstractModel(object):
    """Abstract model of a learning algorithm. When implementing a subclass,
    you have to implement method ``train``. Method ``predict`` is implemented
    by default.
    """

    def __init__(self, feature_selector):
        """Default initializer requires only feature selector to be specified.
        If you want to add additional parameters to your implementation of the
        model, be sure to call this initializer in your initializer first.
        """

        self.feature_selector = feature_selector

    def train(self, documents):
        """Trains the model on the provided list of **labeled** documents.
        This method is expected to initialize field ``predictor``, otherwise
        implemented method predict won't work.
        """

        raise NotImplementedError(
            "Method %s#train not implemented.", self.__class__.__name__)

    def predict(self, document):
        """Predicts label for given document.
        Note that before running this method, method ``train`` must be run.

        :param document: Document to be labeled.
        :returns: Predicted label of the document.
        """

        raise NotImplementedError(
            "Method %s#predict not implemented.", self.__class__.__name__)


class NaiveBayesModel(AbstractModel):
    """Naive Bayes model."""

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
        print predictions.shape
        label = self.feature_selector.get_label(y)

        return label


class SVMModel(AbstractModel):
    """Support Vector Machine model."""

    def __init__(self, feature_selector):
        super(SVMModel, self).__init__(feature_selector)

    def train(self, documents):
        X, Y = self.feature_selector.build(documents)
