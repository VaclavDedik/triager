
def accuracy(model, documents_cv):
    n_cv = len(documents_cv)
    tpn = sum([1 for i in range(n_cv)
              if documents_cv[i].label == model.predict(documents_cv[i])])

    return tpn/float(n_cv)
