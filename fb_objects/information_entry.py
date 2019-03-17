from typing import Dict, Any

from fb_objects.fb_object import FbObject
from webdriver_wrapper import WebDriverWrapper


class InformationEntry(FbObject):
    def __init__(self, name: str, xpath: str, driver: WebDriverWrapper = None):
        super().__init__(driver)
        self._name = name
        self._xpath = xpath
        self._content: str = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def content(self) -> str:
        return self._content

    def parse(self) -> "InformationEntry":
        self._content = self._driver.scrape_text(self._xpath)
        return self

    def serialize(self) -> Dict[str, Any]:
        serialized = {"name": self._name,
                      "xpath": self._xpath,
                      "content": self._content}
        return serialized

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]) -> "InformationEntry":
        entry = InformationEntry(name=serialized["name"], xpath=serialized["xpath"])
        entry._content = serialized["content"]
        return entry

    def set_driver(self, driver: WebDriverWrapper) -> "InformationEntry":
        self._driver = driver
        return self

    def copy(self):
        return InformationEntry(self._name, self._xpath, None)
