from requests import Response
from bugfixpy.jira import api
from bugfixpy.utils import prompt_user
from bugfixpy.utils.text import colors
from .fix_version import FixVersion
from .issue import (
    ApplicationCreationIssue,
    ChallengeCreationIssue,
    ChallengeRequestIssue,
)


class TransitionIssueService:
    def __init__(self) -> None:
        pass

    def transition_chrlq(
        self, challenge_request_issue: ChallengeRequestIssue, fix_message: str
    ) -> None:
        fix_version = api.get_current_fix_version()
        self.__transition_chlrq_to_planned(challenge_request_issue, fix_version)
        self.__transition_chlrq_to_in_progress(challenge_request_issue)
        self.__transition_chlrq_to_closed(challenge_request_issue, fix_message)

    def transition_all_chlcs(
        self,
        application_creation_issue: ApplicationCreationIssue,
        challenge_request_issue: ChallengeRequestIssue,
    ) -> None:
        linked_creation_issues = self.__get_all_linked_creation_issues(
            application_creation_issue
        )
        verifier_id = self.__choose_content_verifier()

        for creation_issue in linked_creation_issues:
            self.transition_chlc(creation_issue, challenge_request_issue, verifier_id)

    def transition_chlc(
        self,
        challenge_creation_issue: ChallengeCreationIssue,
        challenge_request_issue: ChallengeRequestIssue,
        verifier_id: str,
    ) -> None:
        self.__transition_to_feedback_open(challenge_creation_issue)
        self.__transition_to_feedback_review(challenge_creation_issue)
        self.__add_assignee_and_comment(
            challenge_creation_issue, challenge_request_issue, verifier_id
        )

    def __transition_chlrq_to_planned(
        self, challenge_request_issue: ChallengeRequestIssue, fix_version: FixVersion
    ) -> None:
        print(f"\tTo Planned [Fix Version: {fix_version.name}]", end="")
        result = api.transition_challenge_request_to_planned(
            challenge_request_issue, fix_version
        )
        self.__display_transition_result(result)

    def __transition_chlrq_to_in_progress(
        self, challenge_request_issue: ChallengeRequestIssue
    ) -> None:
        print("\tTo In Progress\t\t\t", end="")
        result = api.transition_challenge_request_to_in_progress(
            challenge_request_issue
        )
        self.__display_transition_result(result)

    def __transition_chlrq_to_closed(
        self, challenge_request_issue: ChallengeRequestIssue, fix_message: str
    ) -> None:
        print("\tTo Closed [with description of fix]", end="")
        result = api.transition_challenge_request_to_closed_with_comment(
            challenge_request_issue,
            fix_message,
        )
        self.__display_transition_result(result)

    def __transition_to_feedback_open(self, issue: ChallengeCreationIssue) -> None:
        print("\tTo Feedback Open\t", end="")
        result = api.transition_challenge_creation_to_feedback_open(issue)
        self.__display_transition_result(result)

    def __transition_to_feedback_review(self, issue: ChallengeCreationIssue) -> None:
        print("\tTo Feedback Review\t", end="")
        result = api.transition_challenge_creation_to_feedback_review(issue)
        self.__display_transition_result(result)

    def __choose_content_verifier(self) -> str:
        verifier = prompt_user.to_select_content_verifier()
        name = verifier["name"]
        print(f"\t{name} set as content verifier")
        return verifier["id"]

    def __add_assignee_and_comment(
        self,
        challenge_creation_issue: ChallengeCreationIssue,
        challenge_request_issue: ChallengeRequestIssue,
        content_verifier: str,
    ) -> None:
        print("\tAdding assignee and comment", end="")
        result = api.update_challenge_creation_assignee_and_link_challenge_request(
            challenge_creation_issue,
            challenge_request_issue,
            content_verifier,
        )
        self.__display_transition_result(result)

    def __get_all_linked_creation_issues(
        self, application_creation_issue: ApplicationCreationIssue
    ) -> list[ChallengeCreationIssue]:
        return api.get_challenge_creation_issues_linked_to_application(
            application_creation_issue
        )

    def __display_transition_result(self, result: Response) -> None:
        if result.status_code == 204:
            print("\t✅")
        else:
            print(f"\t❌{colors.FAIL} [{result.reason}]{colors.ENDC}")
