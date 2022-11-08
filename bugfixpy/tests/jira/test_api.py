from datetime import datetime
from unittest import TestCase

from bugfixpy.jira import api
from bugfixpy.jira.issue import (
    ApplicationCreationIssue,
    ChallengeCreationIssue,
    ChallengeRequestIssue,
)


class TestApi(TestCase):
    def test_get_response_code_from_query_to_verify_credentials(self) -> None:
        self.assertEqual(api.get_response_code_from_query_to_verify_credentials(), 200)

    def test_get_current_fix_version(self) -> None:
        today = datetime.now()
        current_version = api.get_current_fix_version()
        month = today.strftime("%b")
        calculated_current_version_name = f"{today.year} {month}"
        self.assertEqual(current_version.name, calculated_current_version_name)

    def test_issue_exists(self) -> None:
        challenge_request = ChallengeRequestIssue("CHLRQ-1234")
        self.assertTrue(api.issue_exists(challenge_request))

        challenge_creation = ChallengeCreationIssue("CHLC-1234")
        self.assertTrue(api.issue_exists(challenge_creation))

        application_creation = ApplicationCreationIssue("CHLC-1234")
        self.assertTrue(api.issue_exists(application_creation))

    def test_transition_challenge_request_to_planned(self) -> None:
        """Need test issue for running this test"""

    def test_transition_challenge_request_to_in_progress(self) -> None:
        """Need test issue for running this test"""

    def test_get_application_creation_related_to_challenge(self) -> None:
        """Need test issue for running this test"""

    def test_get_challenge_creation_issues_linked_to_application(self) -> None:
        """Need test issue for running this test"""

    def test_link_challenge_request_to_challenge_creation_(self) -> None:
        """Need test issue for running this test"""

    def test_transition_challenge_request_to_closed_with_comment(self) -> None:
        """Need test issue for running this test"""

    def test_transition_challenge_creation_to_feedback_open(self) -> None:
        """Need test issue for running this test"""

    def test_transition_challenge_creation_to_feedback_review(self) -> None:
        """Need test issue for running this test"""

    def test_update_challenge_creation_assignee_and_link_challenge_request(
        self,
    ) -> None:
        """Need test issue for running this test"""
