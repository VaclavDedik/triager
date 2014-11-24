
class DocumentParser(object):
    """When implementing a subclass of this class, you are expected to override
    method ``parse``. All parameters that the parse method might need should
    be provided via the initializer.
    """

    def parse(self):
        """This method parses files (or whatever else you set via your
        initializer and returns a list of ``Document`` objects from package
        ``classifier.document``.

        :returns: List of parsed ``Document`` objects.
        """

        raise NotImplementedError()
