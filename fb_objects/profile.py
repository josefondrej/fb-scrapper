from typing import List

from config import *
from fb_objects.fb_object_base import FbObjectBase
from fb_objects.information import Information
from fb_objects.album import Album
from webdriver_wrapper import WebDriverWrapper


class Profile(FbObjectBase):
    def __init__(self, name: str, driver: WebDriverWrapper):
        super().__init__(driver)
        self._name: str = name
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
        url_information = PROFILE_PREFIX + self._name + INFORMATION_SUFFIX
        self._driver.go_to(url_information)
        self._information = Information(self._driver)
        self._driver.back()

        ## todo: url_albums = ...
