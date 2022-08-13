"""
Exception to identify a merge conflict has occurred
"""


class MergeConflictError(Exception):
    """Raise error when cherrypicking branch results in a merge conflict"""
