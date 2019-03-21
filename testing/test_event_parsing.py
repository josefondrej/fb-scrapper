from fb_objects.public_event import PublicEvent
from utils import get_driver

event_url = ""
event_name = ""

driver = get_driver()
driver.go_to(event_url)

event = PublicEvent(event_name, driver=driver)
event.parse()
event.save()
