class InvalidChallengeIdError(Exception):
    """
    Custom exception inherits Exception. Represents error when invalid challenge ID was 
    """
    def __init__(self, message):
        super().__init__(message)