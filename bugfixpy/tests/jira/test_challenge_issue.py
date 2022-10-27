"""Test Jira Issue classes for different types of Jira issues"""

from unittest import TestCase

from bugfixpy.exceptions.invalid_issue_id_exception import InvalidIssueIdException
from bugfixpy.jira import (
    ChallengeRequestIssue,
    ChallengeCreationIssue,
    ApplicationCreationIssue,
    JiraIssue,
)
from bugfixpy.jira.utils import append_project_type_if_not_present


class TestChallengeIssue(TestCase):
    """Test all challenge issue class implementation"""

    VALID_FULL_CHLRQ = "CHLRQ-1234"
    VALID_FULL_CHLC = "CHLC-4321"
    VALID_CHLRQS = [
        "CHLRQ-1",
        "CHLRQ-12",
        "CHLRQ-123",
        "CHLRQ-1234",
        "CHLRQ-12345",
        "1",
        "12",
        "123",
        "1234",
        "12345",
    ]
    VALID_CHLCS = [
        "CHLC-1",
        "CHLC-12",
        "CHLC-123",
        "CHLC-1234",
        "CHLC-12345",
        "1",
        "12",
        "123",
        "1234",
        "12345",
    ]
    INVALID_CHLRQS = [
        "",
        "-",
        "CHLC-",
        "CHLRP-",
        "CHRLQ",
        "CHLRQ-",
        "CHLC-1234",
        "CHLRQ-a",
        "CHLRQ-123z",
        "203fh3",
        "c30h2-29dj",
    ]
    INVALID_CHLCS = [
        "",
        "-",
        "CHLRQ-",
        "CHLP-",
        "CHLC",
        "CHLC-",
        "CHRQ-1234",
        "CHLC-a",
        "CHLC-123z",
        "203fh3",
        "c30h2-29dj",
    ]

    def test_challenge_request_creation(self) -> None:
        """Challenge Request Issue instantiates correctly for valid issue ids"""

        for issue_id in self.VALID_CHLRQS:
            request_issue = ChallengeRequestIssue(issue_id)
            self.assertIsInstance(request_issue, ChallengeRequestIssue)
            self.assertEqual(
                request_issue.get_issue_id(),
                append_project_type_if_not_present(issue_id, JiraIssue.CHLRQ),
            )

    def test_challenge_request_invalid_issue_ids(self) -> None:
        """Challenge Request Issue throws exception for invalid issue ids"""

        for invalid_id in self.INVALID_CHLRQS:
            self.assertRaises(
                InvalidIssueIdException, ChallengeRequestIssue, invalid_id
            )

    def test_challenge_request_project_type(self) -> None:
        """Challenge Request Issue returns correct project type"""

        request_issue = ChallengeRequestIssue(self.VALID_FULL_CHLRQ)
        self.assertEqual(request_issue.get_project_type(), JiraIssue.CHLRQ)

    def test_challenge_creation(self) -> None:
        """Challenge Creation Issue instantiates correctly for valid issue ids"""

        for issue_id in self.VALID_CHLCS:
            creation_issue = ChallengeCreationIssue(issue_id)
            self.assertIsInstance(creation_issue, ChallengeCreationIssue)
            self.assertEqual(
                creation_issue.get_issue_id(),
                append_project_type_if_not_present(issue_id, JiraIssue.CHLC),
            )

    def test_challenge_creation_invalid_issue_ids(self) -> None:
        """Challenge Creation Issue throws exception for invalid issue ids"""

        for invalid_id in self.INVALID_CHLCS:
            self.assertRaises(
                InvalidIssueIdException, ChallengeCreationIssue, invalid_id
            )

    def test_challenge_creation_project_type(self) -> None:
        """Challenge Creation Issue returns correct project type"""

        request_issue = ChallengeCreationIssue(self.VALID_FULL_CHLC)
        self.assertEqual(request_issue.get_project_type(), JiraIssue.CHLC)

    def test_application_creation(self) -> None:
        """Application Creation Issue instantiates correctly for valid issue ids"""

        for issue_id in self.VALID_CHLCS:
            application_issue = ApplicationCreationIssue(issue_id)
            self.assertIsInstance(application_issue, ApplicationCreationIssue)
            self.assertEqual(
                application_issue.get_issue_id(),
                append_project_type_if_not_present(issue_id, JiraIssue.CHLC),
            )

    def test_application_creation_invalid_issue_ids(self) -> None:
        """Application Creation Issue throws exception for invalid issue ids"""

        for invalid_id in self.INVALID_CHLCS:
            self.assertRaises(
                InvalidIssueIdException, ApplicationCreationIssue, invalid_id
            )

    def test_application_creation_project_type(self) -> None:
        """Application Creation Issue returns correct project type"""

        request_issue = ApplicationCreationIssue(self.VALID_FULL_CHLC)
        self.assertEqual(request_issue.get_project_type(), JiraIssue.CHLC)
