from typing import Dict, Any


class Annotation(object):
    def __init__(self, value: float = 0.0):
        self._value = value

    @property
    def value(self):
        return self._value

    def serialize(self):
        return {"value": self._value}

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]) -> "Annotation":
        if serialized is None:
            return None
        return Annotation(serialized["value"])
