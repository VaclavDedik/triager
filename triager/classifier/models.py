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

        x = self.feature_selector.get_x(document)
        predictions = np.dot(self.predictor, x)
        y = predictions.index(max(predictions))
        label = self.feature_selector.get_label(y)

        return label


class SVMModel(AbstractModel):
    """Support Vector Machine model."""

    def __init__(self, feature_selector):
        super(SVMModel, self).__init__(feature_selector)

    def train(self, documents):
        X, Y = self.feature_selector.build(documents)
