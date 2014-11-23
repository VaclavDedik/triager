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
        of provided int representation of the label. It is also expected to
        initialize field ``features`` which contains labels of features
        (usually words). Both field ``labels`` and ``features`` must be sorted
        in ascending order.

        :param documents: List of labeled Document objects.
        :returns: Tuple of X and Y where X is a list of feature vectors for
                  each document and Y a column vector containing labels (in
                  integer).
        """

        raise NotImplementedError(
            "Method %s#build not implemented." % self.__class__.__name__)

    def get_x(self, document):
        """Returns a feature vector for a given document. Default
        implementation counts words in provided document (both in title and
        content together) that occur in the field ``features``.
        Note that before running this method, method ``build`` must be run.

        :param document: Document you want a feature vector for.
        :returns: Feature vector.
        """

        x = []
        word_counts = utils.count_words(
            "%s\n%s" % (document.title, document.content))

        for word in self.features:
            if word in word_counts:
                x.append(word_counts[word])
            else:
                x.append(0)

        return x

    def get_label(self, y):
        """Returns string representation of label for integer representation.
        Note that before running this method, method ``build`` must be run.

        :param y: Integer representation of the label.
        :returns: String representation of the given ``y``.
        """

        return self.labels[y]


class BasicSelector(AbstractSelector):
    """This implementation of feature selector simply creates a feature vector
    from a bag of words. A document is converted into a feature vector by
    simply counting the number of words.
    """

    def __init__(self, min_len=1, min_occur=1):
        self.min_len = min_len
        self.min_occur = min_occur

    def build(self, documents):
        self._build_labels(documents)
        self._build_features(documents)
        X, Y = [], []

        for document in documents:
            x = self.get_x(document)
            y = self.labels.index(document.label)
            X.append(x)
            Y.append(y)

        return np.array(X), np.transpose([Y])

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
        self.features = words

    def _build_labels(self, documents):
        """Builds labels by sorting all unique occurrences of labels in all
        documents.

        :param documents: List of Document objects.
        """

        labels = {document.label for document in documents}
        self.labels = sorted(labels)


class SelectorDecorator(AbstractSelector):
    """Selector decorator allows us to layer more selectors on top of each
    other.
    """

    def __init__(self, selector):
        self.selector = selector

    def build(self, documents):
        X, Y = self.selector.build(documents)
        self.features = list(self.selector.features)
        self.labels = list(self.selector.labels)
        return X, Y


class StandardizationDecorator(SelectorDecorator):
    """Performs Standardization on data by subtracting the mean of each
    feature and dividing by sample standard deviation.
    """

    def build(self, documents):
        X, Y = super(StandardizationDecorator, self).build(documents)
        n = len(X)
        self.m = np.sum(X, axis=0)/float(n)
        self.std = np.std(X, axis=0, ddof=1)
        X_norm = (X - self.m)/self.std

        return X_norm, Y

    def get_x(self, document):
        x = super(StandardizationDecorator, self).get_x(document)
        return (x - self.m)/self.std


class StopWordsDecorator(SelectorDecorator):
    """This decorator removes stop words from feature vector.
    """

    def __init__(self, selector, language='english'):
        super(StopWordsDecorator, self).__init__(selector)
        self.language = language

    def build(self, documents):
        X, Y = super(StopWordsDecorator, self).build(documents)
        stoplist = stopwords.words(self.language)
        remove_lst = []
        new_features = []
        for i, word in enumerate(self.features):
            if word in stoplist:
                remove_lst.append(i)
            else:
                new_features.append(word)

        self.features = new_features
        X_wsw = np.delete(X, remove_lst, axis=1)
        return X_wsw, Y


# TODO: Fix this class
class TFIDFDecorator(SelectorDecorator):
    """Implementation of TF-IDF weighing.
    """

    def get_x(self, document):
        x_counts = self.selector.get_x(document)
        x = []
        for i, word in enumerate(self.features):
            x.append(x_counts[i] * self.word_idfs[word])

        return x

    def _build_features(self, documents):
        self.selector._build_features(documents)
        self.features = self.selector.features

        word_fs = {}
        for doc in documents:
            counts = utils.count_words(doc.title + " " + doc.content)
            for word, _ in counts.iteritems():
                if word in word_fs:
                    word_fs[word] += 1
                else:
                    word_fs[word] = 1

        word_idfs = {}
        for word in self.features:
            if word_fs[word]:
                idf = np.log(len(documents)/float(word_fs[word]))
            else:
                idf = 0
            word_idfs[word] = idf

        self.word_idfs = word_idfs
