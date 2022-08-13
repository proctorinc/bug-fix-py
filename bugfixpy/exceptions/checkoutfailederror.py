"""
Exception to identify a failed checkout occurred
"""


class CheckoutFailedError(Exception):
    """Raise error when checking out to git branch in repository fails"""
