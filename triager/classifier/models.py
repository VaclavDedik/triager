import numpy as np


class AbstractModel(object):
    """Abstract model. When implementing a subclass, you have to implement
    method ``train``. Method ``predict`` is implemented by default.
    """

    def __init__(self, feature_selector):
        self.feature_selector = feature_selector

    def train(self, documents):
        """Trains the model on the provided list of LABELED documents.
        This method is expected to initialize field ``predictor``, otherwise
        implemented method predict won't work."""

        raise NotImplementedError(
            "Method %s#train not implemented.", self.__class__.__name__)

    def predict(self, document):
        x = self.feature_selector.get_x(document)
        predictions = np.dot(self.predictor, x)
        y_i = predictions.index(max(predictions))
        label = self.feature_selector.labels[y_i]
        return label


class SVMModel(AbstractModel):
    def __init__(self, feature_selector):
        super(SVMModel, self).__init__(feature_selector)

    def train(self, documents):
        X, Y = self.feature_selector.build(documents)
