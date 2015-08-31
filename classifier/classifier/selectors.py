import numpy as np

from nltk.corpus import stopwords
from sklearn.decomposition import TruncatedSVD
from sklearn import feature_selection
from sklearn.feature_extraction.text import CountVectorizer

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

        raise NotImplementedError()

    def get_x(self, document):
        """Returns a feature vector for a given document. Default
        implementation counts words in provided document (both in title and
        content together) that occur in the field ``features``.
        Note that before running this method, method ``build`` must be run.

        :param document: Document you want a feature vector for.
        :returns: Feature vector.
        """

        raise NotImplementedError()

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

    def build(self, documents):
        self._build_labels(documents)
        X, Y = [], []

        docs_vector = []
        for document in documents:
            title = document.title if document.title else ""
            content = document.content if document.content else ""
            docs_vector.append(title + "\n" + content)
            Y.append(self.labels.index(document.label))

        self.count_vect = CountVectorizer(decode_error="replace")
        X = np.array(self.count_vect.fit_transform(docs_vector).todense())

        self.features = sorted(self.count_vect.vocabulary_.keys())

        return X, np.transpose([Y])

    def get_x(self, document):
        """Counts words in provided document (both in title and content
        together) that occur in the field ``features``.
        """

        title = document.title if document.title else ""
        content = document.content if document.content else ""
        words = title + "\n" + content
        return np.array(self.count_vect.transform([words]).todense())

    def _build_labels(self, documents):
        """Builds labels by sorting all unique occurrences of labels in all
        documents.

        :param documents: List of Document objects.
        """

        labels = {document.label for document in documents}
        self.labels = sorted(labels)

    def __str__(self):
        return "BasicSelector()"


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

    def get_x(self, document):
        return self.selector.get_x(document)

    def get_label(self, y):
        return self.selector.get_label(y)

    def __str__(self):
        return "->%s" % self.selector


class StandardizationDecorator(SelectorDecorator):
    """Performs Standardization on data by subtracting the mean of each
    feature and dividing by sample standard deviation.
    """

    def build(self, documents):
        X, Y = super(StandardizationDecorator, self).build(documents)
        n = len(X)
        self.m = np.sum(X, axis=0)/float(n)
        self.std = np.std(X, axis=0, ddof=1)
        X_std = (X - self.m)/self.std

        return X_std, Y

    def get_x(self, document):
        x = super(StandardizationDecorator, self).get_x(document)
        return (x - self.m)/self.std

    def __str__(self):
        return "StandardizationDecorator()%s" \
            % super(StandardizationDecorator, self).__str__()


class NormalizationDecorator(SelectorDecorator):
    """Scales all features to unit length."""

    def build(self, documents):
        X, Y = super(NormalizationDecorator, self).build(documents)
        norm = np.sqrt(np.sum(X ** 2, axis=1))
        X_norm = X/np.transpose([norm])
        return X_norm, Y

    def get_x(self, document):
        x = super(NormalizationDecorator, self).get_x(document)
        norm = np.sqrt(np.sum(x ** 2))
        x_norm = x/norm
        return x_norm

    def __str__(self):
        return "NormalizationDecorator()%s" \
            % super(NormalizationDecorator, self).__str__()


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
        self.remove_lst = remove_lst
        X_wsw = np.delete(X, remove_lst, axis=1)
        return X_wsw, Y

    def get_x(self, document):
        x_old = super(StopWordsDecorator, self).get_x(document)
        x = np.delete(x_old, self.remove_lst)
        return x

    def __str__(self):
        return "StopWordsDecorator(language='%s')%s" \
            % (self.language, super(StopWordsDecorator, self).__str__())


class TFIDFDecorator(SelectorDecorator):
    """Implementation of TF-IDF weighing.
    """

    def get_x(self, document):
        x = super(TFIDFDecorator, self).get_x(document)
        return self._tfidf(np.array(x))

    def build(self, documents):
        X, Y = super(TFIDFDecorator, self).build(documents)

        N = len(X)
        fs_d = sum(X > 0)
        self.idfs = np.log(float(N) / fs_d)

        # Method _tfidf can be used on 2D objects if input X is transposed
        # and self.idfs is a column vector
        self.idfs = np.transpose([self.idfs])
        X_tfidf = self._tfidf(X.T).T
        self.idfs = np.concatenate(self.idfs)

        return X_tfidf, Y

    def _tfidf(self, x):
        """Implementation of augumented term frequency to prevent a bias
        towards longer documents.
        """

        n = np.max(x, axis=0)
        x_new = (((x * 0.5) / np.array(n, dtype=float)) + 0.5) * self.idfs

        return x_new

    def __str__(self):
        return "TFIDFDecorator()%s" \
            % super(TFIDFDecorator, self).__str__()


class LSIDecorator(SelectorDecorator):
    """Implementation of a Latent Semantic Indexing feature selector."""

    def __init__(self, selector, k=500):
        super(LSIDecorator, self).__init__(selector)
        self.k = k

    def get_x(self, document):
        x = super(LSIDecorator, self).get_x(document)
        return self.svd.transform(x)[0]

    def build(self, documents):
        X, Y = super(LSIDecorator, self).build(documents)
        self.svd = TruncatedSVD(n_components=self.k, random_state=42)
        self.svd.fit(X)

        return self.svd.transform(X), Y

    def __str__(self):
        return "LSIDecorator(k=%s)%s" \
            % (self.k, super(LSIDecorator, self).__str__())


class ChiSquaredDecorator(SelectorDecorator):
    """Implementation of Chi-Squared feature selection."""

    def __init__(self, selector, threshold=10.86):
        super(ChiSquaredDecorator, self).__init__(selector)
        self.threshold = threshold

    def get_x(self, document):
        x = super(ChiSquaredDecorator, self).get_x(document)
        x_x2 = np.delete(x, self.remove_lst)
        return x_x2

    def build(self, documents):
        X, Y = super(ChiSquaredDecorator, self).build(documents)
        x2, pval = feature_selection.chi2(X, Y)

        self.remove_lst = [
            i for i, val in enumerate(x2) if val < self.threshold]
        X_x2 = np.delete(X, self.remove_lst, axis=1)

        return X_x2, Y

    def __str__(self):
        return "ChiSquaredDecorator(threshold=%s)%s" \
            % (self.threshold, super(ChiSquaredDecorator, self).__str__())
