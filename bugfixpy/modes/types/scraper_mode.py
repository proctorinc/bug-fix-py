import sys

from bugfixpy.cms import (
    ScraperData,
    CmsScraper,
    ApplicationScreenDataWithChallengeBranches,
)
from bugfixpy.exceptions import RequestFailedError
from bugfixpy.utils.text import colors, instructions
from bugfixpy.utils import prompt_user


class ScraperMode:
    cms_scraper: CmsScraper

    def get_scraper_data(self):
        return self.get_scraper_data()

    def get_challenge_data(self, challenge_id: str) -> ScraperData:
        cms_scraper = CmsScraper()
        print("Collecting challenge data from CMS...", end="")
        scraper_data = cms_scraper.scrape_challenge_data(challenge_id)
        print(instructions.DONE)

        return scraper_data

    def get_application_data(
        self, application_name_or_url: str
    ) -> ApplicationScreenDataWithChallengeBranches:
        cms_scraper = CmsScraper()
        print("Collecting application data from CMS...", end="")
        application_data = cms_scraper.scrape_application_data_with_challenge_map(
            application_name_or_url
        )
        print(instructions.DONE)

        return application_data

    def scrape_challenge_data(self) -> ScraperData:
        challenge_data = ScraperData()
        try:
            challenge_id = prompt_user.for_challenge_id()
            challenge_data = self.get_challenge_data(challenge_id)
        except RequestFailedError as err:
            print(f"{colors.FAIL}[Failed]\n{err}{colors.ENDC}")
            sys.exit(1)
        except Exception as err:
            print(f"{colors.FAIL}[Failed]\nUnknown Error: {err}{colors.ENDC}")

        return challenge_data

    def scrape_application_data(self) -> ApplicationScreenDataWithChallengeBranches:
        application_data = ApplicationScreenDataWithChallengeBranches()
        try:
            application_name_or_url: str = prompt_user.for_application_name_or_url()
            application_data = self.get_application_data(application_name_or_url)
        except RequestFailedError as err:
            print(f"{colors.FAIL}[Failed]\n{err}{colors.ENDC}")
            sys.exit(1)
        except Exception as err:
            print(f"{colors.FAIL}[Failed]\nUnknown Error: {err}{colors.ENDC}")

        return application_data
