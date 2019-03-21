from threading import Thread, Lock
from typing import List

from fb_objects.profile import Profile
from fb_objects.public_event import PublicEvent
from utils import get_driver


def load_event_usernames(event_name: str) -> List[str]:
    event = PublicEvent.load(event_name)
    usernames = event.going + event.maybe_going
    return usernames


class Worker(Thread):
    def __init__(self, name: str, usernames: List[str], usernames_lock: Lock):
        Thread.__init__(self)
        self._name = name
        self._usernames = usernames
        self._usernames_lock = usernames_lock
        self._driver = get_driver()
        self.daemon = False

    def run(self):
        while True:
            self._usernames_lock.acquire()
            try:
                username = self._usernames.pop()
            except Exception as e:
                print("[{self._name}] finished")
                self._driver.close()
                break
            self._usernames_lock.release()
            try:
                profile = Profile(username=username, driver=self._driver)
                if Profile.load(username) is None:
                    profile.parse()
                    profile.save()
            except Exception as e:
                print(f"[ERROR] Parsing ({username})")


if __name__ == "__main__":
    WORKERS = 10

    usernames = load_event_usernames("event_name")
    usernames_lock = Lock()

    for i in range(WORKERS):
        worker = Worker(str(i), usernames, usernames_lock)
        worker.start()
