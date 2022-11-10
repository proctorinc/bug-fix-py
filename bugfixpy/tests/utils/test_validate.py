from unittest import TestCase
from ...jira.issue import (
    ApplicationCreationIssue,
    ChallengeCreationIssue,
    ChallengeRequestIssue,
)

from bugfixpy.utils.validate import (
    has_valid_credentials,
    is_valid_challenge_id,
    is_valid_fix_message,
    is_valid_issue,
    is_valid_repository_name,
)

VALID_REPOSITORY_NAMES = [
    "opentasks",
]
INVALID_REPOSITORY_NAMES = [
    "",
]
VALID_FIX_MESSAGES = [
    "this is a valid fix message",
]
INVALID_FIX_MESSAGES = [
    "",
]
VALID_CHALLENGE_IDS = [
    "5dfb305304d5c305ad11fe63",
]
INVALID_CHALLENGE_IDS = [
    "5dfb305304d5c30",
    "5dfb_305304_d5c305a_d11fe63",
    "5dfb305304d5c305ad11fe634f2",
    "5dfb30#304d5c305ad@1fe63",
    "5dfb305304d$c305ad11fe63",
]
VALID_CHLRQS = [
    "CHLRQ-1234",
]
VALID_CHLCS = [
    "CHLC-1234",
]
INVALID_CHLRQS = [
    "CHLRQ-12345",
]
INVALID_CHLCS = [
    "CHLC-12345",
]


class TestValidate(TestCase):
    # def test_is_valid_issue(self) -> None:
    #     for issue_id in VALID_CHLRQS:
    #         print(issue_id)
    #         issue = ChallengeRequestIssue(issue_id)
    #         self.assertTrue(is_valid_issue(issue))

    #     for issue_id in VALID_CHLCS:
    #         issue = ChallengeCreationIssue(issue_id)
    #         self.assertTrue(is_valid_issue(issue))

    #     for issue_id in VALID_CHLCS:
    #         issue = ApplicationCreationIssue(issue_id)
    #         self.assertTrue(is_valid_issue(issue))

    #     for issue_id in INVALID_CHLRQS:
    #         issue = ChallengeRequestIssue(issue_id)
    #         self.assertFalse(is_valid_issue(issue))

    #     for issue_id in INVALID_CHLCS:
    #         issue = ChallengeCreationIssue(issue_id)
    #         self.assertFalse(is_valid_issue(issue))

    #     for issue_id in INVALID_CHLCS:
    #         issue = ApplicationCreationIssue(issue_id)
    #         self.assertFalse(is_valid_issue(issue))

    def test_is_valid_challenge_id(self) -> None:
        for challenge_id in VALID_CHALLENGE_IDS:
            self.assertTrue(is_valid_challenge_id(challenge_id))

        for challenge_id in INVALID_CHALLENGE_IDS:
            self.assertFalse(is_valid_challenge_id(challenge_id))

    def test_is_valid_fix_message(self) -> None:
        for message in VALID_FIX_MESSAGES:
            self.assertTrue(is_valid_fix_message(message))

        for message in INVALID_FIX_MESSAGES:
            self.assertFalse(is_valid_fix_message(message))

    def test_is_valid_repository_name(self) -> None:
        for repository in VALID_REPOSITORY_NAMES:
            self.assertTrue(is_valid_repository_name(repository))

        for repository in INVALID_REPOSITORY_NAMES:
            self.assertFalse(is_valid_repository_name(repository))

    def test_has_valid_credentials(self) -> None:
        # Figure out how to test the case of not having valid credentials
        self.assertTrue(has_valid_credentials())
