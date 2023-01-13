import sys

from bugfixpy.cms import ScraperData, CmsScraper
from bugfixpy.exceptions import RequestFailedError
from bugfixpy.utils.text import colors, instructions
from bugfixpy.utils import prompt_user


class ScraperMode:
    scraper_data: ScraperData
    challenge_id: str

    def get_scraper_data(self) -> ScraperData:
        return self.scraper_data

    def scrape_challenge_data_from_cms(self) -> ScraperData:
        return CmsScraper.scrape_challenge_data(self.challenge_id)

    def scrape_cms_and_print_results(self) -> None:
        print("Collecting data from CMS...", end="")
        self.scraper_data = self.scrape_challenge_data_from_cms()
        print(instructions.DONE)
        print(self.scraper_data)

    def run_scraper(self) -> None:
        try:
            self.challenge_id = prompt_user.for_challenge_id()
            self.scrape_cms_and_print_results()
        except RequestFailedError as err:
            print(f"{colors.FAIL}[Failed]\n{err}{colors.ENDC}")
            sys.exit(1)
        except Exception as err:
            print(
                f"{colors.FAIL}[Failed]\nInvalid challenge ID entered{err}{colors.ENDC}"
            )
