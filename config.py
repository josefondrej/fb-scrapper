# Webdriver Settings
WEBDRIVER_PATH = "/home/josef/Downloads/geckodriver-v0.24.0-linux64/geckodriver"
BINARY_PATH = "/usr/bin/firefox"
MAX_TIMEOUT = 5 # sec
REFRESH_RATE = 0.01 # sec

# Storage
PROFILE_DIR = "./profiles/"
PROFILE_SUFFIX = ".json"

# Facebook General
FB_WWW = "https://m.facebook.com/"
CREDENTIALS_PATH = "credentials.json"
PIC_SUFFIX = ".jpg"

# Login
USERNAME_XPATH = "//input[@id='m_login_email']"
PASSWORD_XPATH = "//input[@type='password']"
LOGIN_XPATH = "//input[@name='login']"
SKIP_PERMAMENT_LOGIN = "/login/save-device/cancel/?flow=interstitial_nux_retry&amp;nux_source=regular_login"

# Profile
INFORMATION_SUFFIX = "/about"
ALBUMS_SUFFIX = "/photos"
FRIENDS_SUFFIX = "/friends"
NAME_XPATH = "/html/body/div/div/div[2]/div/div[1]/div[1]/div[2]/div/span/div/span"
PROFILE_PIC_XPATH = "/html/body/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div/div/a/img"
SHOW_FULL_SIZE_XPATH = "/html/body/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div[2]/span/div/span/a[2]"
PROFILE_PIC_DIR = "./profile_pics/"

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

# Friends
FRIEND_USERNAME_XPATH = "//table/tbody/tr/td[2]/a"
NEXT_FRIENDS_XPATH = "//div[@id='m_more_friends']/a"
FILTERED_USERNAMES = ["policies", "bugnub", "logout.php", "mbasic"]
