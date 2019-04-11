from threading import Thread, Lock
from typing import List, Tuple

from fb_objects.profile import Profile
from fb_objects.public_event import PublicEvent
from utils import get_driver
from webdriver_wrapper import WebDriverWrapper


class Worker(Thread):
    def __init__(self, name: str, usernames: List[str], usernames_lock: Lock, anonymous: bool = True):
        Thread.__init__(self)
        self._name = name
        self._usernames = usernames
        self._usernames_lock = usernames_lock
        self._anonymous = anonymous
        if self._anonymous:
            self._driver = WebDriverWrapper()
        else:
            self._driver = get_driver()
        self.daemon = False

    def run(self):
        while True:
            self._usernames_lock.acquire()
            try:
                username = self._usernames.pop()
            except Exception as e:
                print(f"[{self._name}] finished")
                self._driver.close()
                self._usernames_lock.release()
                break
            self._usernames_lock.release()
            try:
                profile = Profile(username=username, driver=self._driver)
                if Profile.load(username) is None:
                    if self._anonymous:
                        profile.download_profile_picture_anonymous()
                    else:
                        profile.parse()
                    profile.save()
            except:
                print(f"[ERROR] Parsing ({username})")


def argparse() -> Tuple[str, str]:
    import argparse

    parser = argparse.ArgumentParser(description="Parse profiles of people attending some event")
    parser.add_argument("--event-name", help="Name of the event")
    parser.add_argument("--workers", help="Number of threads to use", default=10)

    args = parser.parse_args()

    num_workers = args.workers
    event_name = args.event_name

    return event_name, int(num_workers)


if __name__ == "__main__":
    event_name, num_workers = argparse()
    usernames = PublicEvent.load(event_name).all_usernames
    usernames_lock = Lock()

    for i in range(num_workers):
        worker = Worker("worker " + str(i), usernames, usernames_lock)
        worker.start()
