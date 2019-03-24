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
        self._initialize_friends_going()

        self.get_next()

    def _initialize_filters(self, path: str):
        try:
            with open(path, "r") as file:
                self._filters = json.load(file)
        except IOError:
            self._filters = {"ignore": [], "must_contain": [], "cant_contain": [],
                             "entries": ["basic-info", "education", "relationship"]}

    def _initialize_profile_keywords(self):
        self._profile_keywords = {profile: self._get_profile_keywords(profile) for profile in self._profiles}

    def get_keywords(self, profile: Profile) -> Dict[Profile, List[str]]:
        return self._profile_keywords[profile]

    def _friends_going(self, profile: Profile) -> List[str]:
        friends_going = []
        for username in self._usernames:
            if username in profile.friends:
                friends_going.append(username)

        return friends_going

    def _initialize_friends_going(self):
        self._profile_friends_going = {profile: self._friends_going(profile) for profile in self._profiles}

    def get_friends_going(self, profile: Profile) -> List[str]:
        return self._profile_friends_going[profile]

    def export_filters(self, path: str = None):
        if path is None:
            path = self._filters_path
        with open(path, "w") as file:
            json.dump(self._filters, file)

    def update_ignore(self, keyword: str):
        self._filters["ignore"].append(keyword)

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

    def _get_entry_keywords(self, entry) -> Set[str]:
        keywords = entry.content.split("\n")
        keywords = [k for k in keywords if k not in self._filters["ignore"]]
        return set(keywords)

    def _get_profile_keywords(self, profile: Profile) -> Set[str]:
        keywords = set()
        for entry in profile.information.entries:
            keywords.update(self._get_entry_keywords(entry))

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

    def get_username(self, username: str):
        for i in range(len(self._profiles)):
            profile = self._profiles[i]
            if profile.username == username:
                self._index = i
                return profile

    def current(self) -> Profile:
        current_profile = self._profiles[self._index]
        return current_profile
