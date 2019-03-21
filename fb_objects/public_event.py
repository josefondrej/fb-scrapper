from typing import Any, Dict, List

from utils import parse_usernames
from fb_objects.fb_object import FbObject
from webdriver_wrapper import WebDriverWrapper
from config import GOING_NEXT_XPATH, MAYBE_GOING_NEXT_XPATH, GOING_USERNAMES_XPATH, MAYBE_GOING_USERNAMES_XPATH, \
    EVENT_DIR, EVENT_SUFFIX


class PublicEvent(FbObject):
    _file_dir = EVENT_DIR
    _file_suffix = EVENT_SUFFIX
    _file_name_key = "_name"

    def __init__(self, name: str, driver: WebDriverWrapper = None):
        super().__init__(driver)
        self._name = name
        self._going: List[str] = []
        self._maybe_going: List[str] = []
        self._invited: List[str] = []

    @property
    def name(self):
        return self._name

    @property
    def going(self):
        return self._going

    @property
    def maybe_going(self):
        return self._maybe_going

    def parse(self):
        self._going = parse_usernames(GOING_USERNAMES_XPATH, GOING_NEXT_XPATH, self._driver)
        self._maybe_going = parse_usernames(MAYBE_GOING_USERNAMES_XPATH, MAYBE_GOING_NEXT_XPATH, self._driver)
        return self

    def serialize(self) -> Dict[str, Any]:
        serialized = {"name": self._name,
                      "going": self._going,
                      "maybe_going": self._maybe_going,
                      "invited": self._invited}
        return serialized

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]) -> "PublicEvent":
        public_event = PublicEvent(serialized["name"])
        public_event._going = serialized["going"]
        public_event._maybe_going = serialized["maybe_going"]
        public_event._invited = serialized["invited"]
        return public_event
