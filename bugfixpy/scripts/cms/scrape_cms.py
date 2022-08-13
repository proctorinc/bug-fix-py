"""
CMS Scraping script runs a scraper on the CMS by retrieving the CSRF token, logging into the CMS,
scraping challenge and application screens based off of the challenge ID and returns data.
"""


import sys
from bugfixpy.scraper.cms_scraper import CmsScraper
from bugfixpy.scraper.scraper_data import ScraperData
from bugfixpy.exceptions import RequestFailedError
from bugfixpy.formatter.text import Text
from bugfixpy.constants import colors


def scrape_cms(scraper: CmsScraper) -> ScraperData:
    """
    Scrapes the CMS to retrieve data
    """

    try:
        # Get CSRF token for login
        csrf_token = scraper.fetch_csrf_token()

        # Retrieve cookies from logging into the CMS
        cookies = scraper.login_to_cms(csrf_token)

        # Scrape the challenge screen and return application endpoint
        challenge_screen_data = scraper.scrape_challenge_screen(cookies)

        # Get application endpoint from scraper data
        application_endpoint = challenge_screen_data.application_screen_endpoint

        # Scrape the application screen
        application_screen_data = scraper.scrape_application_screen(
            cookies, application_endpoint
        )

    except RequestFailedError as err:
        Text(f"\n{err}", colors.FAIL).display()
        sys.exit(1)
    except Exception as err:
        Text("\nUnknown Error", err, colors.FAIL).display()
        sys.exit(1)

    return ScraperData(challenge_screen_data, application_screen_data)
