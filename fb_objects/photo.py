from fb_objects.fb_object_base import FbObjectBase
from webdriver_wrapper import WebDriverWrapper


class Photo(FbObjectBase):
    def __init__(self, driver: WebDriverWrapper):
        super().__init__(driver)
