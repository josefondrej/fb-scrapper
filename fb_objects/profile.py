from typing import List

from config import FB_WWW, INFORMATION_SUFFIX, NAME_XPATH
from fb_objects.fb_object_base import FbObjectBase
from fb_objects.information import Information
from fb_objects.album import Album
from webdriver_wrapper import WebDriverWrapper


class Profile(FbObjectBase):
    def __init__(self, username: str, driver: WebDriverWrapper):
        super().__init__(driver)
        self._username: str = username
        self._name: str = None
        self._information: Information = None
        self._albums: List[Album] = None
        self._friends: List[Profile] = None

    @property
    def information(self) -> Information:
        return self._information

    @property
    def albums(self) -> List[Album]:
        return self._albums

    @property
    def friends(self) -> "List[Profile]":
        return self._friends

    def parse(self):
        self._parse_name()

        url_information = FB_WWW + self._username + INFORMATION_SUFFIX
        self._driver.go_to(url_information)
        self._information = Information(self._driver).parse()
        self._driver.back()

        ## todo: url_albums = ...

        return self

    def _parse_name(self):
        self._name = self._driver.scrape_text(NAME_XPATH)


