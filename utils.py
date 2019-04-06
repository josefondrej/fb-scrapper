import json
import os
from typing import Tuple, List

from webdriver_wrapper import WebDriverWrapper
from config import CREDENTIALS_PATH, FB_WWW, LOGIN_XPATH, USERNAME_XPATH, PASSWORD_XPATH, SKIP_PERMAMENT_LOGIN, \
    FILTERED_USERNAMES, PROFILE_DIR, PROFILE_SUFFIX


def load_fb_credentials(credentials_file_path: str) -> Tuple[str, str]:
    credentials = json.load(open(credentials_file_path, "rb"))
    return credentials.get("username"), credentials.get("password")


def list_usernames() -> List[str]:
    raw_usernames = os.listdir(PROFILE_DIR)
    usernames = [username.split(PROFILE_SUFFIX)[0] for username in raw_usernames]
    return usernames


# Facebook Login
def login_to_facebook(driver: WebDriverWrapper):
    username, password = load_fb_credentials(CREDENTIALS_PATH)
    driver.go_to(FB_WWW)
    driver.fill_form(username, USERNAME_XPATH)
    driver.fill_form(password, PASSWORD_XPATH)
    driver.click(LOGIN_XPATH)


def resolve_permanent_login_prompt(driver: WebDriverWrapper):
    driver.go_to(FB_WWW + SKIP_PERMAMENT_LOGIN)


def get_driver() -> WebDriverWrapper:
    driver = WebDriverWrapper()
    login_to_facebook(driver)
    resolve_permanent_login_prompt(driver)
    return driver


# Username parsing
def parse_usernames(username_xpath: str, next_button_xpath: str, driver: WebDriverWrapper):
    usernames = []
    while True:
        try:
            elements = driver._driver.find_elements_by_xpath(username_xpath)
            links = [e.get_attribute("href") for e in elements]
            new_usernames = [_parse_username_from_link(link) for link in links]
            new_usernames = _filter_usernames(new_usernames)
            usernames.extend(new_usernames)
            driver.click(next_button_xpath)
        except Exception as e:
            return usernames


def _filter_usernames(usernames: List[str]):
    filtered_usernames = [username for username in usernames if username not in FILTERED_USERNAMES]
    return filtered_usernames


def _parse_username_from_link(link: str) -> str:
    username = link.split("/")[3].split("?")[0]
    return username


# General
def flatten(lst: List[List]) -> List:
    flat_list = [item for sublist in lst for item in sublist]
    return flat_list
