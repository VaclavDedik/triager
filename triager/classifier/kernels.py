
class AbstractKernel(object):
    """Defines interface of Kernel class."""

    def compute(self, X, Y):
        """Computation of the value of the kernel.

        :param X: Matrix where rows represent instancies and columns represent
                  features.
        :param Y: Labels.
        :returns: Matrix.
        """

        raise NotImplementedError(
            "Method %s#compute not implemented.", self.__class__.__name__)


class GaussianKernel(AbstractKernel):
    """Computes gaussian kernel. This class only works with scikit-learn,
    because at the moment method ``compute`` is not implemented.
    """

    def __init__(self, gamma=0.0):
        self.gamma = gamma
        self.sklearn_name = "rbf"
        self.sklearn_params = {"gamma": self.gamma}
