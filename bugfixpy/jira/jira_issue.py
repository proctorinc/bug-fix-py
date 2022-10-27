"""Challenge Issue Abstract Class"""

from abc import ABC, abstractmethod
import re
from bugfixpy.exceptions import InvalidIssueIdException
from . import utils


class JiraIssue(ABC):
    """
    Abstract class for challenge issues
    """

    CHLRQ = "CHLRQ"
    CHLC = "CHLC"

    __issue_id: str

    def __init__(self, issue_id) -> None:
        """Constructor for challenge issue"""
        if not self.is_valid_issue_id(issue_id):
            raise InvalidIssueIdException()

        self.__issue_id = utils.append_project_type_if_not_present(
            issue_id, self.get_project_type()
        )

    @abstractmethod
    def get_project_type(self):
        """Abstract method for getting the issue type"""

    def get_issue_id(self):
        """Returns the issue id associated this issue"""
        return self.__issue_id

    def is_valid_issue_id(self, issue_id):
        """Validate the issue id based off of the project type"""
        return re.fullmatch(f"({self.get_project_type()}-)?\\d{{1,}}", issue_id)


class ChallengeRequestIssue(JiraIssue):
    """
    Implementation of Jira CHLRQ Issue
    """

    def get_project_type(self):
        return self.CHLRQ


class ChallengeCreationIssue(JiraIssue):
    """
    Implementation of Jira Challenge CHLC Issue
    """

    def get_project_type(self):
        return self.CHLC


class ApplicationCreationIssue(JiraIssue):
    """
    Implementation of Jira Application CHLC Issue
    """

    def get_project_type(self):
        return self.CHLC
