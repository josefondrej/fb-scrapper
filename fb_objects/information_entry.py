from fb_objects.fb_object_base import FbObjectBase
from webdriver_wrapper import WebDriverWrapper


class InformationEntry(FbObjectBase):
    def __init__(self, name: str, xpath: str, driver: WebDriverWrapper):
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

    def set_driver(self, driver: WebDriverWrapper) -> "InformationEntry":
        self._driver = driver
        return self
