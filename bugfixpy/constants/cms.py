import os
from dotenv import load_dotenv

load_dotenv()

# CMS email
EMAIL = os.getenv("CMS_EMAIL")

# CMS password
PASSWORD = os.getenv("CMS_PASSWORD")

# URL for CMS
URL = "https://cms.securecodewarrior.com"

# URL to login to the CMS
LOGIN_URL = f"{URL}/login"

# URL to search for challenge in CMS
SEARCH_URL = f"{URL}/search"
