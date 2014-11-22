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
