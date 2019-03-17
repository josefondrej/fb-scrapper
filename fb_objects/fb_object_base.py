from typing import Dict, Any
from webdriver_wrapper import WebDriverWrapper


class FbObjectBase(object):
    def __init__(self, driver: WebDriverWrapper = None):
        self._driver = driver

    def parse(self) -> "FbObjectBase":
        raise NotImplementedError("Has to be overriden.")

    def serialize(self) -> Dict[str, Any]:
        raise NotImplementedError("Has to be overriden.")

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]) -> "FbObjectBase":
        raise NotImplementedError("Has to be overriden.")
