"""Challenge Issue Abstract Class"""

from abc import ABC, abstractmethod

from bugfixpy.exceptions import InvalidIssueIdException


class JiraIssue(ABC):
    """
    Abstract class for challenge issues
    """

    __issue_id: str

    def __init__(self, issue_id) -> None:
        """Constructor for challenge issue"""
        if not self.is_valid():
            raise InvalidIssueIdException()

        __issue_id = issue_id


    def get_issue_id(self):
        """Returns the issue id associated this issue"""
        return self.__issue_id


    @abstractmethod
    def get_project_type(self):
        """Abstract method for getting the issue type"""


    @abstractmethod
    def is_valid(self):
        """Abstract method for validating"""

class ChallengeRequestIssue(JiraIssue):
    """
    Implementation of Jira CHLRQ Issue
    """

    CHLRQ = "CHLRQ"

    def get_project_type(self):
        return self.CHLRQ

    def is_valid(self):
        """Abstract method for validating"""
        return True


class ChallengeCreationIssue(JiraIssue):
    """
    Implementation of Jira Challenge CHLC Issue
    """

    CHLC = "CHLC"

    def get_project_type(self):
        return self.CHLC

    def is_valid(self):
        """Abstract method for validating"""
        return True

class ApplicationCreationIssue(JiraIssue):
    """
    Implementation of Jira Application CHLC Issue
    """

    CHLC = "CHLC"

    def get_project_type(self):
        return self.CHLC

    def is_valid(self):
        """Abstract method for validating"""
        return True
