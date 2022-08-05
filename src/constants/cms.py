import os
from dotenv import load_dotenv

load_dotenv()

#############################
# CMS webscraping constants #
#############################

# CMS email
CMS_EMAIL = os.getenv("CMS_EMAIL")

# CMS password
CMS_PASSWORD = os.getenv("CMS_PASSWORD")

# URL for CMS
CMS_URL = "https://cms.securecodewarrior.com"

# URL to login to the CMS
CMS_LOGIN_URL = f"{CMS_URL}/login"

# URL to search for challenge in CMS
CMS_SEARCH_URL = f"{CMS_URL}/search"
