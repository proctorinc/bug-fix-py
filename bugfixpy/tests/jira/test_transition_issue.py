from unittest import TestCase
from unittest.mock import Mock, patch

from bugfixpy.jira import (
    ChallengeRequestIssue,
    ChallengeCreationIssue,
    ApplicationCreationIssue,
    TransitionIssues,
)
from bugfixpy.cms import (
    ApplicationScreenData,
    ChallengeScreenData,
    ScraperData,
)
from bugfixpy.git import FixResult


class TestTransitionIssues(TestCase):

    CHALLENGE_REQUEST = ChallengeRequestIssue("CHLRQ-1234")
    CHALLENGE_CREATION = ChallengeCreationIssue("CHLC-3456")
    APPLICATION_CREATION = ApplicationCreationIssue("CHLC-5678")
    CHALLENGE_ID = "5dfb305304d5c305ad11fe63"
    FIX_RESULT = FixResult(["test fix"], False, False)
    CHALLENGE_SCREEN_DATA = ChallengeScreenData("~", CHALLENGE_CREATION)
    APPLICATION_SCREEN_DATA = ApplicationScreenData(APPLICATION_CREATION, "mock-repo")
    CHALLENGE_DATA = ScraperData(CHALLENGE_SCREEN_DATA, APPLICATION_SCREEN_DATA)

    __transition_issues: TransitionIssues

    def setUp(self) -> None:
        self.__transition_issues = TransitionIssues(
            self.FIX_RESULT, self.CHALLENGE_DATA, self.CHALLENGE_REQUEST
        )

    def test_run(self) -> None:
        self.__transition_issues.run()
