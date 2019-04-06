from typing import Any


class ProfileFilterBase(object):
    def __init__(self):
        pass

    def matches(self, profile: Any):
        """ Filter allows profile to pass through it

          :param profile: Profile or string representing username """
        raise NotImplementedError("Has to be overriden")
