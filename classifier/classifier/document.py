
class Document(object):
    """Class that represents a text document that is to be classified."""

    def __init__(self, title, content, label=None):
        self.title = title
        self.content = content
        self.label = label
