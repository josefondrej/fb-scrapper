from webdriver_wrapper import WebDriverWrapper


class FbObjectBase(object):
    def __init__(self, driver: WebDriverWrapper):
        self._driver = driver

    def parse(self) -> "FbObjectBase":
        raise NotImplementedError("Has to be overriden.")

    def serialize(self) -> str:
        raise NotImplementedError("Has to be overriden.")

    def deserialize(self, serialized_representation: str) -> "FbObjectBase":
        raise NotImplementedError("Has to be overriden.")