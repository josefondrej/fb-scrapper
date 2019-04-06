import json
import time
from threading import Thread, Lock
from typing import List, Set

import utils
from config import WORKER_POOL_CACHE
from fb_objects.profile import Profile
from profile_filters import InformationFilter
from utils import get_driver


class Worker(Thread):
    def __init__(self, name: str, usernames: Set[str], usernames_lock: Lock,
                 usernames_parsed: Set[str], usernames_parsed_lock: Lock,
                 profile_filter: InformationFilter = None,
                 release_on_empty_usernames: bool = False):
        Thread.__init__(self)
        self._name = name
        self._usernames = usernames
        self._usernames_lock = usernames_lock
        self._usernames_parsed = usernames_parsed
        self._usernames_parsed_lock = usernames_parsed_lock
        self._profile_filter = profile_filter
        self._release_on_empty_usernames = release_on_empty_usernames

        self._driver = get_driver()
        self.daemon = False

    def run(self):
        while True:
            username = None
            with self._usernames_lock:
                if self._usernames:
                    username = self._usernames.pop()

            if username is None:
                if self._release_on_empty_usernames:
                    print(f"[{self._name}] finished")
                    self._driver.close()
                    break
                else:
                    time.sleep(1.0)
                    continue
            else:
                with self._usernames_parsed_lock:
                    username_parsed = username in self._usernames_parsed

                if not username_parsed:
                    try:
                        profile = Profile(username=username, driver=self._driver)
                        profile._parse_information()

                        if self._profile_filter is not None and self._profile_filter.matches(profile):
                            profile.parse()
                            profile.save()

                        with self._usernames_parsed_lock:
                            self._usernames_parsed.add(username)
                    except:
                        print(f"[ERROR] Parsing ({username})")


class WorkerPool(object):
    def __init__(self, num_workers: int = 10, profile_filter: InformationFilter = None,
                 release_on_empty_usernames: bool = False):
        self._num_workers = num_workers
        self._release_on_empty_usernames = release_on_empty_usernames
        self._usernames = set()
        self._usernames_lock = Lock()
        self._usernames_parsed = set()
        self._usernames_parsed_lock = Lock()
        self._load_cache()
        self._profile_filter = profile_filter
        self._workers = [self._make_worker(f"worker {i}") for i in range(self._num_workers)]

    def extend(self, usernames: List[str]):
        new_usernames = usernames - self._usernames_parsed
        if not new_usernames:
            self._dump_cache()
            raise AssertionError("No new usernames to parse")

        with self._usernames_lock:
            self._usernames = self._usernames.update(new_usernames)

    def add(self, username: str):
        with self._usernames_lock:
            if username not in self._usernames_parsed:
                self._usernames.add(username)

    def _make_worker(self, name: str) -> "Worker":
        return Worker(name=name,
                      usernames=self._usernames,
                      usernames_lock=self._usernames_lock,
                      usernames_parsed=self._usernames_parsed,
                      usernames_parsed_lock=self._usernames_parsed_lock,
                      profile_filter=self._profile_filter,
                      release_on_empty_usernames=self._release_on_empty_usernames)

    def start(self):
        for worker in self._workers:
            worker.start()

    def _dump_cache(self):
        cache = {"usernames_parsed": list(self._usernames_parsed)}
        json.dump(cache, open(WORKER_POOL_CACHE, "w"))

    def _load_cache(self):
        self._usernames_parsed = self._usernames_parsed.union(utils.list_usernames())
        try:
            cache = json.load(open(WORKER_POOL_CACHE, "r"))
            self._usernames_parsed = self._usernames_parsed.union(cache.get("usernames_parsed"))
            print("[INFO] Worker pool cache loaded successfully")
        except:
            print("[INFO] Worker pool cache not found")
