import json
from typing import Tuple

from fb_objects.profile import Profile
from webdriver_wrapper import WebDriverWrapper
from config import CREDENTIALS_PATH, FB_WWW, LOGIN_XPATH, USERNAME_XPATH, PASSWORD_XPATH, SKIP_PERMAMENT_LOGIN, \
    PROFILE_DIR, PROFILE_SUFFIX


def load_fb_credentials(credentials_file_path: str) -> Tuple[str, str]:
    credentials = json.load(open(credentials_file_path, "rb"))
    return credentials.get("username"), credentials.get("password")


# Facebook Login
def login_to_facebook(driver: WebDriverWrapper):
    username, password = load_fb_credentials(CREDENTIALS_PATH)
    driver.go_to(FB_WWW)
    driver.fill_form(username, USERNAME_XPATH)
    driver.fill_form(password, PASSWORD_XPATH)
    driver.click(LOGIN_XPATH)


def resolve_permanent_login_prompt(driver: WebDriverWrapper):
    driver.go_to(FB_WWW + SKIP_PERMAMENT_LOGIN)


# Saving / Loading Data from Disc
def save_profile(profile: Profile):
    path = PROFILE_DIR + profile._username + PROFILE_SUFFIX
    serialized_profile = profile.serialize()
    json.dump(serialized_profile, open(path, "w"))


def load_profile(username: str) -> Profile:
    path = PROFILE_DIR + username + PROFILE_SUFFIX
    try:
        serialized_profile = json.load(open(path, "r"))
        profile = Profile.deserialize(serialized_profile)
        return profile
    except IOError:
        print(f"[utils] Profile `{username}` not in database")
        return None
