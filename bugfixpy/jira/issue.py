from abc import ABC, abstractmethod
import re
from bugfixpy.exceptions import InvalidIssueIdError
from . import utils


class Issue(ABC):
    """Abstract class for challenge issues"""

    CHLRQ = "CHLRQ"
    CHLC = "CHLC"

    __issue_id: str

    def __init__(self, issue_id) -> None:
        if not self.is_valid_issue_id(issue_id):
            raise InvalidIssueIdError()

        self.__issue_id = utils.append_project_type_if_not_present(
            issue_id, self.get_project_type()
        )

    @abstractmethod
    def get_project_type(self) -> str:
        pass

    def get_issue_id(self) -> str:
        return self.__issue_id

    def is_valid_issue_id(self, issue_id) -> bool:
        issue_id_with_or_without_project_type = (
            f"({self.get_project_type()}-)?\\d{{1,}}"
        )
        return bool(re.fullmatch(issue_id_with_or_without_project_type, issue_id))

    def get_issue_endpoint(self) -> str:
        issue_id = self.get_issue_id()
        return f"/issue/{issue_id}"

    def get_transition_endpoint(self) -> str:
        issue_endpoint = self.get_issue_endpoint()
        return issue_endpoint + "/transitions"


class ChallengeRequestIssue(Issue):
    def get_project_type(self) -> str:
        return self.CHLRQ


class ChallengeCreationIssue(Issue):
    def get_project_type(self) -> str:
        return self.CHLC


class ApplicationCreationIssue(Issue):
    def get_project_type(self) -> str:
        return self.CHLC
