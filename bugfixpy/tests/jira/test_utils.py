"""Jira utility method tests"""

from unittest import TestCase

from bugfixpy.jira.utils import append_project_type_if_not_present
from bugfixpy.jira.jira_issue import JiraIssue


class TestUtils(TestCase):
    """Test Jira utility methods"""

    VALID_INCOMPLETE_ISSUE_NUMBERS = [
        "1",
        "12",
        "123",
        "1234",
        "12345",
    ]
    VALID_COMPLETE_CHLC_ISSUE_NUMBERS = [
        "CHLC-1",
        "CHLC-12",
        "CHLC-123",
        "CHLC-1234",
        "CHLC-12345",
    ]
    VALID_COMPLETE_CHLRQ_ISSUE_NUMBERS = [
        "CHLRQ-1",
        "CHLRQ-12",
        "CHLRQ-123",
        "CHLRQ-1234",
        "CHLRQ-12345",
    ]

    def test_incomplete_input_on_append_project_type_if_not_present(self) -> None:
        """Test that project type appends to incomplete issue number"""

        for i, incomplete_issue in enumerate(self.VALID_INCOMPLETE_ISSUE_NUMBERS):
            self.assertEqual(
                append_project_type_if_not_present(incomplete_issue, JiraIssue.CHLC),
                self.VALID_COMPLETE_CHLC_ISSUE_NUMBERS[i],
            )

        for i, incomplete_issue in enumerate(self.VALID_INCOMPLETE_ISSUE_NUMBERS):
            self.assertEqual(
                append_project_type_if_not_present(incomplete_issue, JiraIssue.CHLRQ),
                self.VALID_COMPLETE_CHLRQ_ISSUE_NUMBERS[i],
            )

    def test_complete_input_on_append_project_type_if_not_present(self) -> None:
        """Test that project type append to issue number"""

        for complete_issue in self.VALID_COMPLETE_CHLRQ_ISSUE_NUMBERS:
            self.assertEqual(
                append_project_type_if_not_present(complete_issue, JiraIssue.CHLRQ),
                complete_issue,
            )

        for complete_issue in self.VALID_COMPLETE_CHLC_ISSUE_NUMBERS:
            self.assertEqual(
                append_project_type_if_not_present(complete_issue, JiraIssue.CHLC),
                complete_issue,
            )
