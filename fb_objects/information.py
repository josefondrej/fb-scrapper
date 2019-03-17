from fb_objects.fb_object_base import FbObjectBase
from fb_objects.information_entry import InformationEntry
from webdriver_wrapper import WebDriverWrapper
from config import ENTRIES


class Information(FbObjectBase):
    registered_entries = []

    @classmethod
    def register(cls, name: str, xpath: str):
        cls.registered_entries.append(InformationEntry(name, xpath, None))

    def __init__(self, webdriver: WebDriverWrapper):
        super().__init__(webdriver)
        self._entries = []

    def parse(self, verbose: bool = False) -> "Information":
        if verbose:
            print(f"[{self._username}]")
        for registered_entry in Information.registered_entries:
            entry = registered_entry.copy()
            entry.set_driver(self._driver)
            entry.parse()
            self._entries.append(entry)
            # except Exception as e:
            #     if verbose:
            #         print(f"\t `{registered_entry.name}` -- not located")
        return self

    def get_entry(self, name: str):
        for entry in self._entries:
            if entry.name == name:
                return entry
        return None


for entry in ENTRIES:
    Information.register(entry["name"], entry["xpath"])
