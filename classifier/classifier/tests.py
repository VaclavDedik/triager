import numpy as np


def accuracy(model, documents_cv, n=1):
    """Computes accuracy of the model.

    :param model: Prediction model.
    :param documents_cv: List of documents.
    :param n: Number of "suggested" options.
    """
    n_cv = len(documents_cv)
    tpn = sum([1 for i in range(n_cv)
              if documents_cv[i].label in model.predict(documents_cv[i], n=n)])

    return tpn/float(n_cv)


def precision_and_recall(model, documents_cv):
    """Computes macro average precision and recall.

    :param model: Prediction model.
    :param documents_cv: List of documents.
    """

    labels = list(model.feature_selector.labels)
    # If there are labels that are not in the train set
    for document in documents_cv:
        if document.label not in labels:
            labels.append(document.label)

    n_c = len(labels)
    tpi = np.zeros(n_c)
    fpi = np.zeros(n_c)
    fni = np.zeros(n_c)

    for document in documents_cv:
        plabel = model.predict(document)[0]
        if document.label == plabel:
            tpi[labels.index(document.label)] += 1
        else:
            fpi[labels.index(plabel)] += 1
            fni[labels.index(document.label)] += 1

    # Fix division by zero
    for i, tp in enumerate(tpi):
        if tp == 0:
            fpi[i], fni[i] = 1, 1

    precisioni = tpi/(tpi+fpi)
    recalli = tpi/(tpi+fni)
    precision = sum(precisioni)/n_c
    recall = sum(recalli)/n_c

    return (precision, recall)


def fscore(precision, recall):
    """Computes F1-score based on precision and recall."""

    fscore = 0.0
    if precision + recall > 0:
        fscore = 2*(precision*recall)/(precision+recall)

    return fscore
