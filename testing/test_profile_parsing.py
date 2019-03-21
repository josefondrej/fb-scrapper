from fb_objects.profile import Profile
from utils import get_driver

username = ""

driver = get_driver()

profile = Profile(username=username, driver=driver)
profile.parse()

profile.save()
profile = Profile.load(username)

print(profile)
