from unittest import TestCase
from unittest.mock import Mock, patch

from requests import Response

from bugfixpy.jira import (
    ChallengeRequestIssue,
    ChallengeCreationIssue,
    ApplicationCreationIssue,
    TransitionIssues,
    FixVersion,
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
    FIX_VERSION = FixVersion("version_id", "version_name")
    FIX_MESSAGE = "test fix"
    FIX_RESULT = FixResult([FIX_MESSAGE], False, False)
    CHALLENGE_SCREEN_DATA = ChallengeScreenData("~", CHALLENGE_CREATION)
    APPLICATION_SCREEN_DATA = ApplicationScreenData(APPLICATION_CREATION, "mock-repo")
    CHALLENGE_DATA = ScraperData(CHALLENGE_SCREEN_DATA, APPLICATION_SCREEN_DATA)

    @patch("bugfixpy.jira.api.transition_challenge_request_to_planned")
    @patch(
        "bugfixpy.jira.api.transition_challenge_request_to_in_progress",
    )
    @patch(
        "bugfixpy.jira.api.transition_challenge_request_to_closed_with_comment",
    )
    @patch(
        "bugfixpy.jira.api.transition_challenge_creation_to_feedback_open",
    )
    @patch(
        "bugfixpy.jira.api.transition_challenge_creation_to_feedback_review",
    )
    @patch(
        "bugfixpy.jira.api.update_challenge_creation_assignee_and_link_challenge_request",
    )
    @patch(
        "bugfixpy.jira.api.get_current_fix_version",
        return_value=FIX_VERSION,
    )
    @patch("bugfixpy.utils.prompt_user.to_press_enter_to_transition_request_issue")
    @patch("bugfixpy.utils.prompt_user.to_press_enter_to_transition_creation_issues")
    def test_run(
        self,
        mock_prompt_transition_creation,
        mock_prompt_transition_request,
        get_fix_version,
        update_assignee_and_link,
        transition_feedback_review,
        transition_feedback_open,
        transition_closed,
        transition_in_progress,
        transition_planned,
    ) -> None:
        mock_response = Response()
        mock_response.status_code = 204

        transition_planned.return_value = mock_response
        transition_in_progress.return_value = mock_response
        transition_closed.return_value = mock_response
        transition_feedback_open.return_value = mock_response
        transition_feedback_review.return_value = mock_response
        update_assignee_and_link.return_value = mock_response
        get_fix_version.return_value = FixVersion("version_id", "version_name")

        transition_issues = TransitionIssues(
            self.FIX_RESULT, self.CHALLENGE_DATA, self.CHALLENGE_REQUEST
        )

        transition_issues.run()
        transition_planned.assert_called_with(self.CHALLENGE_REQUEST, self.FIX_VERSION)
        transition_in_progress.assert_called_with(self.CHALLENGE_REQUEST)
        transition_closed.assert_called_with(self.CHALLENGE_REQUEST, self.FIX_MESSAGE)
        transition_feedback_open.assert_called_with(self.CHALLENGE_CREATION)
        transition_feedback_review.assert_called_with(self.CHALLENGE_CREATION)
        update_assignee_and_link.assert_called_with(
            self.CHALLENGE_CREATION, self.CHALLENGE_REQUEST
        )
        get_fix_version.assert_called_once()
        mock_prompt_transition_request.assert_called_once()
        mock_prompt_transition_creation.assert_called_once()
