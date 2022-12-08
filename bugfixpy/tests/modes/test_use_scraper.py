import unittest
from unittest.mock import Mock, patch
from bugfixpy.jira.issue import ApplicationCreationIssue, ChallengeCreationIssue
from bugfixpy.classes import UseScraper
from bugfixpy.scraper import (
    ApplicationScreenData,
    ChallengeScreenData,
    ScraperData,
)


class TestUseScraper(unittest.TestCase):

    mock_scraper_data = ScraperData(
        ChallengeScreenData(
            application_endpoint="", chlc=ChallengeCreationIssue("CHLC-1234")
        ),
        ApplicationScreenData(
            chlc=ApplicationCreationIssue("CHLC-5678"), repository_name="opentasks"
        ),
    )

    @patch(
        "bugfixpy.utils.prompt_user.for_challenge_id",
        return_value="5dfb305304d5c305ad11fe63",
    )
    def test_run_scraper(self, patched) -> None:
        MockUseScraper = UseScraper
        MockUseScraper.scrape_challenge_data_from_cms = Mock(
            return_value=self.mock_scraper_data
        )
        challenge_id = "5dfb305304d5c305ad11fe63"
        scraper = MockUseScraper()
        scraper.run_scraper()
        data = scraper.get_scraper_data()
        challenge_creation_issue_id = data.challenge.chlc.get_issue_id()
        application_creation_issue_id = data.application.chlc.get_issue_id()
        self.assertEqual(challenge_creation_issue_id, "CHLC-1234")
        self.assertEqual(application_creation_issue_id, "CHLC-5678")
