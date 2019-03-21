from typing import List, Dict, Any

from fb_objects.fb_object import FbObject
from fb_objects.photo import Photo
from webdriver_wrapper import WebDriverWrapper


class Album(FbObject):
    def __init__(self, name: str, driver: WebDriverWrapper = None):
        super().__init__(driver)
        self._name = name
        self._photos: List[Photo] = None

    def parse(self):
        pass  # todo: implement

    def serialize(self) -> Dict[str, Any]:
        serialized = {"name": self._name, "photos": [photo.serialize() for photo in self._photos]}
        return serialized

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]):
        album = Album(serialized["name"])
        for photo in serialized["photos"]:
            album._photos.append(Photo.deserialize(photo))
