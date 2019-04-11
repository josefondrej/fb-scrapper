import json
from typing import Dict, Any
from webdriver_wrapper import WebDriverWrapper


class FbObject(object):
    _file_dir = None
    _file_suffix = None
    _file_name_key = None

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
    def _path_to_file(cls, key):
        path = cls._file_dir + key + cls._file_suffix
        return path

    @property
    def _key(self):
        return self.__getattribute__(self.__class__._file_name_key)

    def save(self):
        path = self.__class__._path_to_file(self._key)
        serialized = self.serialize()
        json.dump(serialized, open(path, "w"))

    @classmethod
    def load(cls, key: str, verbose=False) -> "FbObject":
        path = cls._path_to_file(key)
        try:
            serialized = json.load(open(path, "r"))
            fb_object = cls.deserialize(serialized)
            return fb_object
        except IOError:
            if verbose:
                print(f"[ERROR] Object ({key})[{cls.__name__}] not in database")
            return None

    def set_driver(self, driver: WebDriverWrapper):
        self._driver = driver

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
