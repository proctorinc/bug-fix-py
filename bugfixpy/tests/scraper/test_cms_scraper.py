# from bugfixpy.scripts.cms import scrape_cms
import unittest

from bugfixpy.exceptions import RequestFailedError
from bugfixpy.scraper import CmsScraper

# Test constants
VALID_CHALLENGE_ID = "5dfb305304d5c305ad11fe63"
INVALID_CHALLENGE_ID = "@#(7y2!#&-=3!84"
INVALID_CSRF_TOKEN = "X"
INVALID_CREDENTIALS = ("fake", "password")


class TestCmsScraper(unittest.TestCase):
    """Test class for CmsScraper class"""

    def test_valid_challenge_id(self) -> None:
        """Tests valid input for CMS Scraper"""

        scraper = CmsScraper(VALID_CHALLENGE_ID)
        self.assertIsInstance(scraper, CmsScraper)

    def test_invalid_challenge_id(self) -> None:
        """Tests invalid input for CMS Scraper"""

        self.assertRaises(ValueError, CmsScraper, INVALID_CHALLENGE_ID)

    def test_fetch_csrf_token(self) -> None:
        """Tests that fetch_csrf_token() fetches the CSRF token successfully"""

        scraper = CmsScraper(VALID_CHALLENGE_ID)
        csrf_token = scraper.fetch_csrf_token()

        self.assertNotEqual(csrf_token, "")

    def test_login_to_cms_valid(self) -> None:
        """
        Test valid login to CMS. This test is dependent on the keyring credentials being valid
        """

        scraper = CmsScraper(VALID_CHALLENGE_ID)
        csrf_token = scraper.fetch_csrf_token()
        scraper.login_to_cms(csrf_token)

        self.assertIsInstance(scraper, CmsScraper)

    def test_login_to_cms_invalid_csrf_token(self) -> None:
        """Test invalid csrf login to CMS"""

        scraper = CmsScraper(VALID_CHALLENGE_ID)
        self.assertRaises(RequestFailedError, scraper.login_to_cms, INVALID_CSRF_TOKEN)

    def test_login_to_cms_invalid_credentials(self) -> None:
        """Test invalid credentials login to CMS"""

        scraper = CmsScraper(VALID_CHALLENGE_ID, credentials=INVALID_CREDENTIALS)
        csrf_token = scraper.fetch_csrf_token()
        self.assertRaises(RequestFailedError, scraper.login_to_cms, csrf_token)

    def test_scrape_challenge_screen(self) -> None:
        """Test that scraping the challenge screen collects data successfully"""

        # Create scraper

        # Get csrf_token

        # Login to cms

        # Run scraping challenge screen

        # Assert that scraped data exists

    def test_scrape_application_screen(self) -> None:
        """Test that scraping the application screen collects data successfully"""

        # Create scraper

        # Get csrf_token

        # Login to cms

        # Run scraping challenge screen

        # Run scraping application screen

        # Assert that scraped data exists

    def test_update_application_branches(self) -> None:
        """Test that updating the application branches runs successfully"""

        # Create scraper

        # Get csrf_token

        # Login to cms

        # Run scraping challenge screen????

        # Run scraping application screen????

        # Update application branches

        # Assert that scraped data exists


if __name__ == "__main__":
    unittest.main()
