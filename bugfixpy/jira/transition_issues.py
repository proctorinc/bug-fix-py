from typing import Callable
from requests import Response

from bugfixpy.constants import colors
from bugfixpy.scraper import ScraperData
from bugfixpy.git import FixResult
from bugfixpy.jira import api
from bugfixpy import utils

from .fix_version import FixVersion
from .issue import (
    ApplicationCreationIssue,
    ChallengeCreationIssue,
    ChallengeRequestIssue,
    Issue,
)


class TransitionIssues:

    __challenge_request_issue: ChallengeRequestIssue
    __challenge_creation_issue: ChallengeCreationIssue
    __application_creation_issue: ApplicationCreationIssue
    __repo_was_cherrypicked: bool
    __fix_version: FixVersion
    __fix_message: str

    def __init__(
        self,
        fix_result: FixResult,
        challenge_data: ScraperData,
        challenge_request_issue: ChallengeRequestIssue,
    ) -> None:
        self.__challenge_request_issue = challenge_request_issue
        self.__challenge_creation_issue = challenge_data.challenge.chlc
        self.__application_creation_issue = challenge_data.application.chlc
        self.__repo_was_cherrypicked = fix_result.repo_was_cherrypicked
        self.__fix_version = api.get_current_fix_version()
        self.__fix_message = utils.combine_messages_into_string(fix_result.fix_messages)
        self.__creation_issues = self.__get_creation_issues_to_transition()

    def run(self) -> None:
        input(
            f"\nPress {colors.OKGREEN}[Enter]{colors.ENDC} to auto transition {colors.OKCYAN}{self.__challenge_request_issue.get_issue_id()}{colors.ENDC}"
        )
        self.__transition_request_issue()
        input(
            f"\nPress {colors.OKGREEN}[Enter]{colors.ENDC} to auto transition [{colors.OKBLUE}{len(self.__creation_issues)}{colors.ENDC}] {colors.HEADER}CHLCs{colors.ENDC}"
        )
        self.__transition_creation_issues()

    def __get_creation_issues_to_transition(self) -> list[ChallengeCreationIssue]:
        if self.__repo_was_cherrypicked:
            return api.get_challenge_creation_issues_linked_to_application(
                self.__application_creation_issue
            )

        return [self.__challenge_creation_issue]

    def __transition_request_issue(self) -> None:
        print(
            f"\nTransitioning {colors.OKCYAN}{self.__challenge_request_issue.get_issue_id()}{colors.ENDC}"
        )
        self.__transition_to_planned()
        self.__transition_to_in_progress()
        self.__transition_to_closed()

    def __transition_to_planned(self) -> None:
        print(f"\tTo Planned [Fix Version: {self.__fix_version.name}]", end="")
        self.__transition_issue(
            self.__challenge_request_issue,
            api.transition_challenge_request_to_planned,
            self.__fix_version,
        )

    def __transition_to_in_progress(self) -> None:
        print("\tTo In Progress\t\t\t", end="")
        self.__transition_issue(
            self.__challenge_request_issue,
            api.transition_challenge_request_to_in_progress,
        )

    def __transition_to_closed(self) -> None:
        print("\tTo Closed [with description of fix]", end="")
        self.__transition_issue(
            self.__challenge_request_issue,
            api.transition_challenge_request_to_closed_with_comment,
            self.__fix_message,
        )

    def __transition_creation_issues(self) -> None:
        for issue in self.__creation_issues:
            print(f"Transitioning {colors.HEADER}{issue.get_issue_id()}{colors.ENDC}:")
            self.__transition_creation_issue(issue)

    def __transition_creation_issue(self, issue) -> None:
        self.__transition_to_feedback_open(issue)
        self.__transition_to_feedback_review(issue)
        self.__add_assignee_and_comment(issue)

    def __transition_to_feedback_open(self, issue: ChallengeCreationIssue) -> None:
        print("\tTo Feedback Open\t", end="")
        self.__transition_issue(
            issue,
            api.transition_challenge_creation_to_feedback_open,
        )

    def __transition_to_feedback_review(self, issue: ChallengeCreationIssue) -> None:
        print("\tTo Feedback Review\t", end="")
        self.__transition_issue(
            issue,
            api.transition_challenge_creation_to_feedback_review,
        )

    def __add_assignee_and_comment(self, issue: ChallengeCreationIssue) -> None:
        print("\tAdding assignee and comment", end="")
        self.__transition_issue(
            issue,
            api.update_challenge_creation_assignee_and_link_challenge_request,
            self.__challenge_request_issue,
        )

    def __transition_issue(
        self, issue: Issue, transition_function: Callable, *params
    ) -> None:
        result = transition_function(issue, params)
        self.__display_transition_result(result)

    def __display_transition_result(self, result: Response) -> None:
        if result.status_code == 204:
            print("\t✅")
        else:
            print(f"\t❌{colors.FAIL} [{result.reason}]{colors.ENDC}")
