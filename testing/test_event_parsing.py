from fb_objects.public_event import PublicEvent
from utils import get_driver

event_name = "event_name"
event_url = "https://m.facebook.com/events/1234567/permalink/guests/?filter=others"

driver = get_driver()
driver.go_to(event_url)

event = PublicEvent(event_name, driver=driver)
event.parse()
event.save()
