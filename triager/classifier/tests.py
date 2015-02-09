import numpy as np


def accuracy(model, documents_cv):
    n_cv = len(documents_cv)
    tpn = sum([1 for i in range(n_cv)
              if documents_cv[i].label == model.predict(documents_cv[i])])

    return tpn/float(n_cv)


def precision_and_recall(model, documents_cv, avg=True):
    labels = model.feature_selector.labels
    n_c = len(labels)
    tpi = np.zeros(n_c)
    fpi = np.zeros(n_c)
    fni = np.zeros(n_c)

    for document in documents_cv:
        plabel = model.predict(document)
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

    if not avg:
        return (precisioni, recalli)
    else:
        precision = sum(precisioni)/n_c
        recall = sum(recalli)/n_c
        return (precision, recall)