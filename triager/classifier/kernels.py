import numpy as np


class AbstractKernel(object):
    """Defines interface of Kernel class."""

    def compute(self, x, x0):
        """Computation of the similarity value of the kernel.

        :param x: Represents an instance of X.
        :param x0: Represents another instance of X.
        :returns: Similarity value of the instances.
        """

        raise NotImplementedError()


class LinearKernel(AbstractKernel):
    """Computes linear similarity value."""

    def __init__(self):
        self.sklearn_name = "linear"
        self.sklearn_params = {}

    def compute(self, x, x0):
        return np.dot(x, np.transpose([x0]))

    def __str__(self):
        return "LinearKernel()"


class PolynomialKernel(AbstractKernel):
    """computes polynomial similarity value."""

    def __init__(self, r=1, d=1):
        self.r = r
        self.d = d
        self.sklearn_name = "poly"
        self.sklearn_params = {"degree": self.d, "coef0": self.r}

    def compute(self, x, x0):
        return (self.gamma * np.dot(x, np.transpose([x0])) + self.r) ** self.d

    def __str__(self):
        return "PolynomialKernel(r=%s, d=%s)" % (self.r, self.d)


class GaussianKernel(AbstractKernel):
    """Computes gaussian kernel. This class only works with scikit-learn,
    because at the moment method ``compute`` is not implemented.
    """

    def __init__(self, gamma=0.0):
        self.gamma = gamma
        self.sklearn_name = "rbf"
        self.sklearn_params = {"gamma": self.gamma}

    def __str__(self):
        return "GaussianKernel(gamma=%s)" % self.gamma
