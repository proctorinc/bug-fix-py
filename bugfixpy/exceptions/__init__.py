"""
Exceptions for all project module to specify errors from CmsScraper and GitRepository classes
"""


from .request_failed_error import RequestFailedError
from .checkout_failed_error import CheckoutFailedError
from .merge_conflict_error import MergeConflictError
from .invalid_issue_id_exception import InvalidIssueIdException
