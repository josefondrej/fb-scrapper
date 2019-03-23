from typing import List

from fb_objects.profile import Profile


class ProfileServer(object):
    def __init__(self, usernames: List[str]):
        self._usernames = usernames
        self._index = 0
        self._current_profile = None

    def _get(self, shift: int):
        self._index += shift
        self._index = self._index % len(self._usernames)
        username = self._usernames[self._index]
        self._current_profile = Profile.load(username)
        return self._current_profile

    def get_next(self) -> Profile:
        return self._get(+1)

    def get_prev(self) -> Profile:
        return self._get(-1)
