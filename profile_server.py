import json
from typing import List, Dict, Set

from fb_objects.profile import Profile


class ProfileServer(object):
    def __init__(self, usernames: List[str], filters_path: str = "filters.json"):
        self._usernames = usernames
        self._profiles = self._load_profiles(self._usernames)
        self._index: int = 0
        self._filters_path = filters_path

        self._initialize_filters(self._filters_path)
        self._initialize_profile_keywords()

    def _initialize_filters(self, path: str):
        try:
            with open(path, "rb") as file:
                self._filters = json.load(file)
        except IOError:
            self._filters = {"ignore": [], "must_contain": [], "cant_contain": [],
                             "entries": ["basic-info", "education", "relationship"]}

    def _initialize_profile_keywords(self):
        self._profile_keywords = {profile: self._get_profile_keywords(profile) for profile in self._profiles}

    def _get_keywords(self, profile: Profile) -> Dict[Profile, List[str]]:
        return self._profile_keywords[profile]

    def _export_filters(self, path: str):
        with open(path, "wb") as file:
            json.dump(self._filters, file)

    def _satisfies_filters(self, profile: Profile) -> bool:
        profile_keywords = self._get_profile_keywords(profile)

        for keyword in self._filters["cant_contain"]:
            if keyword in profile_keywords:
                return False

        if not self._filters["must_contain"]:
            return True

        # must contain = must contain at least one
        for keyword in self._filters["must_contain"]:
            if keyword in profile_keywords:
                return True

        return False

    def _parse_entry_keywords(self, entry) -> Set[str]:
        keywords = entry.content.split("\n")
        keywords = [k for k in keywords if k not in self._filters["ignore"]]
        return set(keywords)

    def _get_profile_keywords(self, profile: Profile) -> Set[str]:
        keywords = set()
        for entry in profile.information.entries:
            keywords.update(self._parse_entry_keywords(entry))

        return keywords

    def _load_profiles(self, usernames: List[str]) -> List[Profile]:
        profiles = []
        for username in usernames:
            profile = Profile.load(username)
            profiles.append(profile)

        return profiles

    def _get(self, shift: int) -> Profile:
        k = 0
        while k <= len(self._profiles):
            self._index += shift
            self._index = self._index % len(self._usernames)
            profile = self._profiles[self._index]
            if self._satisfies_filters(profile):
                return profile
            k += 1

        return Profile(username="[ERROR] No profile satisfying filters")

    def get_next(self) -> Profile:
        return self._get(+1)

    def get_prev(self) -> Profile:
        return self._get(-1)
