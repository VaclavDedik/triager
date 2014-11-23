import numpy as np

from nltk.corpus import stopwords

import utils


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

        self.labels = self._build_labels(documents)
        self.features = self._build_features(documents)
        X, Y = [], []

        for document in documents:
            x = self.get_x(document)
            y = self.labels.index(document.label)
            X.append(x)
            Y.append(y)

        return np.array(X), np.transpose([Y])

    def get_x(self, document):
        """Returns a feature vector for a given document.
        Note that before running this method, method ``build`` must be run.

        :param document: Document you want a feature vector for.
        :returns: Feature vector.
        """

        raise NotImplementedError(
            "Method %s#get_x not implemented." % self.__class__.__name__)

    def get_label(self, y):
        """Returns string representation of label for integer representation.
        Note that before running this method, method ``build`` must be run.

        :param y: Integer representation of the label.
        :returns: String representation of the given ``y``.
        """

        return self.labels[y]

    def _build_labels(self, documents):
        """Default implementation of _build_labels builds labels by sorting
        all unique occurrences of labels in all documents

        :param documents: List of Document objects.
        :returns: List of labels (classes/categories).
        """

        labels = {document.label for document in documents}
        return sorted(labels)

    def _build_features(self, documents):
        """Builds features from a list of documents.
        :param documents: List of Document objects.
        :returns: List of features.
        """

        raise NotImplementedError(
            "Method %s#_build_features not implemented."
            % self.__class__.__name__)


class BasicSelector(AbstractSelector):
    """This implementation of feature selector simply creates a feature vector
    from a bag of words. A document is converted into a feature vector by
    simply counting the number of words.
    """

    def __init__(self, min_len=2, min_occur=2):
        self.min_len = min_len
        self.min_occur = min_occur

    def get_x(self, document):
        """Counts words in provided document (both in title and summary
        together) that occur in the feature vector.
        """

        x = np.zeros(len(self.features))
        word_counts = utils.count_words(
            "%s\n%s" % (document.title, document.content))

        for word, count in word_counts.items():
            if word in self.features:
                x_i = self.features.index(word)
                x[x_i] = count
        return x

    def _build_features(self, documents):
        """Concatenates all document titles and content together and creates
        a feature vector from all the words in it. Words that occur in the
        list of documents less then ``min_occur`` times are removed and so are
        words that are shorter than ``min_len``.
        """

        consolidated = ""
        for document in documents:
            consolidated += document.title + "\n"
            consolidated += document.content + "\n"

        words = sorted(
            [w for w, c in utils.count_words(consolidated).iteritems()
             if c >= self.min_occur])
        words = [w for w in words if len(w) >= self.min_len]
        return words


class SelectorDecorator(AbstractSelector):
    """Selector decorator allows us to layer more selectors on top of each
    other.
    """

    def __init__(self, selector):
        self.selector = selector

    def build(self, documents):
        return self.selector.build(documents)

    def get_x(self, document):
        return self.selector.get_x(document)

    def get_label(self, y):
        return self.selector.get_label(y)

    def _build_labels(self, documents):
        return self.selector._build_labels(documents)

    def _build_features(self, documents):
        return self.selector._build_features(documents)


class StopWordsDecorator(SelectorDecorator):
    """This decorator removes stop words from feature vector.
    """

    def __init__(self, selector, language='english'):
        super(StopWordsDecorator, self).__init__(selector)
        self.language = language

    def _build_features(self, documents):
        words = self.selector._build_features(documents)
        stoplist = stopwords.words(self.language)
        words_sl = [f for f in words if f.lower() not in stoplist]
        return words_sl
