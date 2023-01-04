import sys

from bugfixpy.cms import ScraperData, CmsScraper
from bugfixpy.exceptions import RequestFailedError
from bugfixpy.utils.text import colors
from bugfixpy.utils import prompt_user, Text


class ScraperMode:
    scraper_data: ScraperData
    challenge_id: str

    def get_scraper_data(self) -> ScraperData:
        return self.scraper_data

    def scrape_challenge_data_from_cms(self) -> ScraperData:
        return CmsScraper.scrape_challenge_data(self.challenge_id)

    def print_scraper_data(self, scraper_data) -> None:
        Text("[Done]", colors.OKGREEN).display()
        Text(
            "Challenge CHLC:", scraper_data.challenge.chlc.get_issue_id(), colors.OKCYAN
        ).display()
        Text(
            "Application CHLC:",
            scraper_data.application.chlc.get_issue_id(),
            colors.OKCYAN,
        ).display()
        Text("Repo:", scraper_data.application.repository_name, colors.OKCYAN).display()

    def print_scraper_results(self) -> None:
        self.print_scraper_data(self.scraper_data)

    def scrape_cms_and_print_results(self) -> None:
        print("Collecting data from CMS...", end="")
        self.scraper_data = self.scrape_challenge_data_from_cms()
        self.print_scraper_results()

    def run_scraper(self) -> None:
        try:
            self.challenge_id = prompt_user.for_challenge_id()
            self.scrape_cms_and_print_results()
        except RequestFailedError as err:
            Text(f"[Failed]\n{err}", colors.FAIL).display()
            sys.exit(1)
        except Exception as err:
            Text(f"[Failed]\nInvalid challenge ID entered{err}", colors.FAIL).display()
