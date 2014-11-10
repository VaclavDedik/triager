import re
import numpy as np


class AbstractSelector(object):
    """Abstract feature selector. When implementing a subclass, you have to
    implement method ``build`` that builds a vector of features X labeled by Y.
    """

    def build(self, documents):
        """This method is used to build features and labels from **labeled**
        documents and return a feature vector with a label for each document.
        This method is expected to initialize field ``labels`` which is used
        by default implementation of ``get_label`` to get string representation
        of provided int representation of the label.

        :param documents: List of labeled Document objects.
        :returns: Tuple of X and Y where X is a list of feature vectors for
                  each document and Y a column vector containing labels (in
                  integer).
        """

        raise NotImplementedError(
            "Method %s#build not implemented.", self.__class__.__name__)

    def get_x(self, document):
        """Returns a feature vector for a given document.
        Note that before running this method, method ``build`` must be run.

        :param document: Document you want a feature vector for.
        :returns: Feature vector.
        """

        raise NotImplementedError(
            "Method %s#get_x not implemented.", self.__class__.__name__)

    def get_label(self, y):
        """Returns string representation of label for integer representation.
        Note that before running this method, method ``build`` must be run.

        :param y: Integer representation of the label.
        :returns: String representation of the given ``y``.
        """

        return self.labels[y]

    def _build_labels(self, documents):
        labels = {document.label for document in documents}
        self.labels = sorted(labels)


class BasicSelector(AbstractSelector):
    """This implementation of feature selector simply creates a feature vector
    from a bag of words. A document is converted into a feature vector by
    simply counting the number of words.
    """

    def build(self, documents):
        """Builds feature vector from words contained in all provided
        documents (concatenates document title with content).
        """

        self._build_labels(documents)
        self._build_features(documents)
        X, Y = [], []

        for document in documents:
            x = self.get_x(document)
            y = self.labels.index(document.label)
            X.append(x)
            Y.append(y)

        return np.array(X), np.transpose([Y])

    def get_x(self, document):
        """Counts words in provided document (both in title and summary
        together).
        """

        x = np.zeros(len(self.features))
        word_counts = self._count_words(
            "%s\n%s" % (document.title, document.content))

        for word, count in word_counts.items():
            if word in self.features:
                x_i = self.features.index(word)
                x[x_i] = count
        return x

    def _build_features(self, documents):
        consolidated = ""
        for document in documents:
            consolidated += document.title + "\n"
            consolidated += document.content + "\n"

        words = sorted(self._count_words(consolidated).keys())
        self.features = words

    def _count_words(self, text):
        word_counts = {}
        removed_symbols = re.sub('[^a-zA-Z]', ' ', text)
        words = removed_symbols.lower().split()

        for word in words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

        return word_counts
