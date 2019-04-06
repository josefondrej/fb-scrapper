import re
from typing import Any
from fb_objects.profile import Profile
from profile_filters.ProfileFilterBase import ProfileFilterBase


class InformationFilter(ProfileFilterBase):
    def __init__(self, name: str = None):
        self._name = name
        self._patterns = []

    def add(self, entry: str = "education", regexp: str = "regexp") -> "InformationFilter":
        self._patterns.append({"entry": entry, "regexp": regexp})
        return self

    def matches(self, profile: Any) -> bool:
        if isinstance(profile, Profile):
            return self._matches_profile(profile)
        elif isinstance(profile, str):
            return self._matches_profile_username(profile)
        else:
            raise ValueError("[ERROR] InformationFilter can only match arg of type Profile or str")

    def _matches_profile(self, profile: Profile) -> bool:
        for pattern in self._patterns:
            entry = pattern["entry"]
            regexp = pattern["regexp"]
            entry = profile.information.get_entry(entry)
            if entry is not None and re.findall(regexp, entry.content.lower()):
                return True

        return False

    def _matches_profile_username(self, username: str) -> bool:
        profile = Profile.load(username)
        return self._matches_profile(profile)
