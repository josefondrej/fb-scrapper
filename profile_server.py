from typing import List

from fb_objects.profile import Profile


class ProfileServer(object):
    def __init__(self, usernames: List[str]):
        self._usernames = usernames
        self._index = 0
        self._current_profile = None

    def get_next(self) -> Profile:
        username = self._usernames[self._index]
        self._current_profile = Profile.load(username)
        self._index += 1
        self._index = self._index % len(self._usernames)
        return self._current_profile
