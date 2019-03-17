import json
from typing import Tuple
from webdriver_wrapper import WebDriverWrapper
from config import CREDENTIALS_PATH, FB_WWW, LOGIN_XPATH, USERNAME_XPATH, PASSWORD_XPATH, SKIP_PERMAMENT_LOGIN


def load_fb_credentials(credentials_file_path: str) -> Tuple[str, str]:
    credentials = json.load(open(credentials_file_path, "rb"))
    return credentials.get("username"), credentials.get("password")


def login_to_facebook(driver: WebDriverWrapper):
    username, password = load_fb_credentials(CREDENTIALS_PATH)
    driver.go_to(FB_WWW)
    driver.fill_form(username, USERNAME_XPATH)
    driver.fill_form(password, PASSWORD_XPATH)
    driver.click(LOGIN_XPATH)


def resolve_permanent_login_prompt(driver: WebDriverWrapper):
    driver.go_to(FB_WWW + SKIP_PERMAMENT_LOGIN)
