from fb_objects.profile import Profile
from fb_objects.public_event import PublicEvent
from utils import get_driver

event_name = ""

driver = get_driver()

event = PublicEvent.load(event_name)

for username in (event.going + event.maybe_going):
    try:
        profile = Profile(username=username, driver=driver)
        if Profile.load(username) is None:
            profile.parse()
            profile.save()
    except Exception as e:
        print(f"[ERROR] Parsing ({username})")
