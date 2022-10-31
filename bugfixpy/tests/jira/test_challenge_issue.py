"""Test Jira Issue classes for different types of Jira issues"""

from unittest import TestCase

from bugfixpy.exceptions.invalid_issue_id_error import InvalidIssueIdError
from bugfixpy.jira import (
    ChallengeRequestIssue,
    ChallengeCreationIssue,
    ApplicationCreationIssue,
    Issue,
)
from bugfixpy.jira.utils import append_project_type_if_not_present

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


class TestChallengeRequestIssue(TestCase):
    def test_challenge_request_creation(self) -> None:
        for issue_id in VALID_CHLRQS:
            request_issue = ChallengeRequestIssue(issue_id)
            self.assertIsInstance(request_issue, ChallengeRequestIssue)
            self.assertEqual(
                request_issue.get_issue_id(),
                append_project_type_if_not_present(issue_id, Issue.CHLRQ),
            )

    def test_challenge_request_invalid_issue_ids(self) -> None:
        for invalid_id in INVALID_CHLRQS:
            self.assertRaises(InvalidIssueIdError, ChallengeRequestIssue, invalid_id)

    def test_challenge_request_project_type(self) -> None:
        request_issue = ChallengeRequestIssue(VALID_FULL_CHLRQ)
        self.assertEqual(request_issue.get_project_type(), Issue.CHLRQ)


class TestChallengeCreationIssue(TestCase):
    def test_challenge_creation(self) -> None:
        for issue_id in VALID_CHLCS:
            creation_issue = ChallengeCreationIssue(issue_id)
            self.assertIsInstance(creation_issue, ChallengeCreationIssue)
            self.assertEqual(
                creation_issue.get_issue_id(),
                append_project_type_if_not_present(issue_id, Issue.CHLC),
            )

    def test_challenge_creation_invalid_issue_ids(self) -> None:
        for invalid_id in INVALID_CHLCS:
            self.assertRaises(InvalidIssueIdError, ChallengeCreationIssue, invalid_id)

    def test_challenge_creation_project_type(self) -> None:
        request_issue = ChallengeCreationIssue(VALID_FULL_CHLC)
        self.assertEqual(request_issue.get_project_type(), Issue.CHLC)


class TestApplicationCreationIssue(TestCase):
    def test_application_creation(self) -> None:
        for issue_id in VALID_CHLCS:
            application_issue = ApplicationCreationIssue(issue_id)
            self.assertIsInstance(application_issue, ApplicationCreationIssue)
            self.assertEqual(
                application_issue.get_issue_id(),
                append_project_type_if_not_present(issue_id, Issue.CHLC),
            )

    def test_application_creation_invalid_issue_ids(self) -> None:
        for invalid_id in INVALID_CHLCS:
            self.assertRaises(InvalidIssueIdError, ApplicationCreationIssue, invalid_id)

    def test_application_creation_project_type(self) -> None:
        request_issue = ApplicationCreationIssue(VALID_FULL_CHLC)
        self.assertEqual(request_issue.get_project_type(), Issue.CHLC)
