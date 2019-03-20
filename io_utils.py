import json
from config import PROFILE_DIR, PROFILE_SUFFIX, EVENT_DIR, EVENT_SUFFIX
from fb_objects.profile import Profile
from fb_objects.public_event import PublicEvent


# Saving / Loading Data from Disc
# todo: rewrite using one general method

def save_profile(profile: Profile):
    path = PROFILE_DIR + profile._username + PROFILE_SUFFIX
    serialized_profile = profile.serialize()
    json.dump(serialized_profile, open(path, "w"))


def load_profile(username: str) -> Profile:
    path = PROFILE_DIR + username + PROFILE_SUFFIX
    try:
        serialized_profile = json.load(open(path, "r"))
        profile = Profile.deserialize(serialized_profile)
        return profile
    except IOError:
        print(f"[utils] Profile `{username}` not in database")
        return None


def save_event(public_event: PublicEvent):
    path = EVENT_DIR + public_event.name + EVENT_SUFFIX
    serialized_event = public_event.serialize()
    json.dump(serialized_event, open(path, "w"))


def load_event(name: str) -> PublicEvent:
    path = PROFILE_DIR + name + PROFILE_SUFFIX
    try:
        serialized_event = json.load(open(path, "r"))
        profile = PublicEvent.deserialize(serialized_event)
        return profile
    except IOError:
        print(f"[utils] Event `{name}` not in database")
        return None
