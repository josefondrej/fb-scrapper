from typing import List

from fb_objects.fb_object_base import FbObjectBase
from fb_objects.photo import Photo
from webdriver_wrapper import WebDriverWrapper


class Album(FbObjectBase):
    def __init__(self, name: str, driver: WebDriverWrapper):
        super().__init__(driver)
        self._name = name
        self._photos: List[Photo] = None
