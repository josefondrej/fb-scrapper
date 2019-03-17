from typing import Dict, Any, Callable
from webdriver_wrapper import WebDriverWrapper


class FbObject(object):
    def __init__(self, driver: WebDriverWrapper = None):
        self._driver = driver

    def __str__(self):
        return str(self.serialize())

    def parse(self) -> "FbObject":
        raise NotImplementedError("Has to be overriden.")

    def serialize(self) -> Dict[str, Any]:
        raise NotImplementedError("Has to be overriden.")

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]) -> "FbObject":
        raise NotImplementedError("Has to be overriden.")

    @classmethod
    def _magic_serialize(cls, obj: "FbObject") -> Dict[str, Any]:
        if obj is None:
            return None

        if isinstance(obj, list):
            return [i.serialize() for i in obj]
        else:
            return obj.serialize()

    @classmethod
    def _magic_deserialize(cls, obj: Dict[str, Any], factory: "todo: what should go here?"):
        if obj is None:
            return None

        if isinstance(obj, list):
            return [factory.deserialize(i) for i in obj]
        else:
            return factory.deserialize(obj)
