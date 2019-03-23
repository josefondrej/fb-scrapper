from typing import Tuple

from fb_objects.public_event import PublicEvent
from utils import get_driver


def parse_event(event_name: str, event_url: str):
    driver = get_driver()
    driver.go_to(event_url)

    event = PublicEvent(event_name, driver=driver)
    event.parse()
    event.save()

    driver.close()


def argparse() -> Tuple[str, str]:
    import argparse

    parser = argparse.ArgumentParser(description="Parse usernames of people attending some event")
    parser.add_argument("--url",
                        help="Event url (https://m.facebook.com/events/1234567/permalink/guests/?filter=others)",
                        default=10)
    parser.add_argument("--event-name", help="Your name for the event", default="some_event")

    args = parser.parse_args()

    event_name = args.event_name
    event_url = args.url

    return event_name, event_url


if __name__ == "__main__":
    event_name, event_url = argparse()
    parse_event(event_name, event_url)
