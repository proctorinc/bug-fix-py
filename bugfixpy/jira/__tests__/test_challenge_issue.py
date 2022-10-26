"""Test"""

import unittest

from jira import ChallengeRequestIssue, ChallengeCreationIssue, ApplicationCreationIssue

class TestChallengeIssue(unittest.TestCase):
    """Test"""

    def test_challenge_request_creation(self) -> None:
        """Test"""
        request_issue = ChallengeRequestIssue("CHRLQ-0000")

        self.assertIsInstance(request_issue, ChallengeRequestIssue)

    def test_challenge_creation(self) -> None:
        """Test"""
        creation_issue = ChallengeCreationIssue("CHLC-0000")

        self.assertIsInstance(creation_issue, ChallengeRequestIssue)

    def test_application_creation(self) -> None:
        """Test"""
        creation_issue = ApplicationCreationIssue("CHLC-0000")

        self.assertIsInstance(creation_issue, ChallengeRequestIssue)
