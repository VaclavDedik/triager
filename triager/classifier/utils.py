import re


def count_words(text):
    word_counts = {}
    removed_symbols = re.sub("[']+", '', text)
    removed_symbols = re.sub("[^a-zA-Z]", ' ', removed_symbols)
    words = removed_symbols.lower().split()

    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    return word_counts


def filter_docs(documents, min_class_occur=1):
    """Filters documents that don't satisfy minimum number of classes
    condition.
    """

    occurrences = {}
    for doc in documents:
        if doc.label in occurrences:
            occurrences[doc.label] += 1
        else:
            occurrences[doc.label] = 1
    filtered_docs = filter(
        lambda d: occurrences[d.label] >= min_class_occur, documents)

    return filtered_docs
