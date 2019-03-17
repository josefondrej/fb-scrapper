from typing import Any, Dict

from fb_objects.fb_object import FbObject
from webdriver_wrapper import WebDriverWrapper


class Photo(FbObject):
    def __init__(self, driver: WebDriverWrapper = None):
        super().__init__(driver)

    def parse(self):
        pass  # todo: implement

    def serialize(self) -> Dict[str, Any]:
        serialized = {}
        return serialized

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]) -> "Photo":
        photo = Photo()
        return photo
