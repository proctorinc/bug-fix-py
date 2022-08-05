class RequestFailedError(Exception):
    """
    Custom exception inherits Exception. Represents error while requesting API or scraping CMS
    """

    def __init__(self, message):
        super().__init__(message)
