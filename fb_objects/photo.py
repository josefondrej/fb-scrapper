from typing import Any, Dict

from fb_objects.fb_object_base import FbObjectBase
from webdriver_wrapper import WebDriverWrapper


class Photo(FbObjectBase):
    def __init__(self, driver: WebDriverWrapper = None):
        super().__init__(driver)

    def serialize(self) -> Dict[str, Any]:
        serialized = {}
        return serialized

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]) -> "Photo":
        photo = Photo()
        return photo
