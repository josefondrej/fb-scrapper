# Webdriver Settings
WEBDRIVER_PATH = "/home/josef/Downloads/geckodriver-v0.24.0-linux64/geckodriver"
BINARY_PATH = "/usr/bin/firefox"

# Storage
PROFILE_DIR = "./fb_scraper/profiles/"

# Facebook General
FB_WWW = "https://m.facebook.com/"
CREDENTIALS_PATH = "credentials.json"

# Login
USERNAME_XPATH = "//input[@id='m_login_email']"
PASSWORD_XPATH = "//input[@type='password']"
LOGIN_XPATH = "//input[@name='login']"
SKIP_PERMAMENT_LOGIN = "/login/save-device/cancel/?flow=interstitial_nux_retry&amp;nux_source=regular_login"

# Profile
INFORMATION_SUFFIX = "/about"
ALBUMS_SUFFIX = "/photos"
FRIENDS_SUFFIX = "/friends"
NAME_XPATH = "//h3"

# Information
ENTRIES = [
    {"name": "work", "xpath": "//div[@id='work']"},
    {"name": "education", "xpath": "//div[@id='education']"},
    {"name": "relationship", "xpath": "//div[@id='relationship']"},
    {"name": "living", "xpath": "//div[@id='living']"},
    {"name": "contact-info", "xpath": "//div[@id='contact-info']"},
    {"name": "basic-info", "xpath": "//div[@id='basic-info']"},
    {"name": "nicknames", "xpath": "//div[@id='nicknames']"},
    {"name": "family", "xpath": "//div[@id='family']"},
    {"name": "year-overviews", "xpath": "//div[@id='year-overviews']"},
    {"name": "interested-in", "xpath": "//div[@id='interested-in']"},
    {"name": "religion", "xpath": "//div[@id='religion']"},
    {"name": "politics", "xpath": "//div[@id='politics']"},
    {"name": "quote", "xpath": "//div[@id='quote']"}
]
