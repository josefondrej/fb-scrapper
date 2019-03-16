from fb_objects.profile import Profile
from webdriver_wrapper import WebDriverWrapper

driver = WebDriverWrapper()
profile = Profile(name="josef.ondrej", driver=driver).parse()
education = profile.information.get_entry("education").content
print(education)

