from typing import List, Dict, Any

from config import FB_WWW, INFORMATION_SUFFIX, ALBUMS_SUFFIX, FRIENDS_SUFFIX, NAME_XPATH
from fb_objects.fb_object_base import FbObjectBase
from fb_objects.information import Information
from fb_objects.album import Album
from webdriver_wrapper import WebDriverWrapper


class Profile(FbObjectBase):
    def __init__(self, username: str, driver: WebDriverWrapper = None):
        super().__init__(driver)
        self._username: Profile = Profile(username)
        self._name: str = None
        self._information: Information = None
        self._albums: List[Album] = None
        self._friends: List[Profile] = None

    @property
    def information(self) -> Information:
        return self._information

    @property
    def albums(self) -> List[Album]:
        return self._albums

    @property
    def friends(self) -> "List[Profile]":
        return self._friends

    def parse(self):
        self._parse_name()

        url_information = FB_WWW + self._username + INFORMATION_SUFFIX
        self._driver.go_to(url_information)
        self._information = Information(self._driver).parse()

        url_albums = FB_WWW + self._username + ALBUMS_SUFFIX
        self._driver.go_to(url_albums)
        self._albums = []
        album_links = self._parse_album_links()
        for name, link in album_links.items():
            self._driver.go_to(link)
            album = Album(name=name, driver=self._driver).parse()
            self._albums.append(album)
            self._driver.back()

        url_friends = FB_WWW + self._username + FRIENDS_SUFFIX
        self._driver.go_to(url_friends)
        friend_usernames = self._parse_friend_usernames()
        for username in friend_usernames:
            self._friends.append(Profile(username=username))

        return self

    def serialize(self) -> Dict[str, Any]:
        serialized = {"username": self._username,
                      "name": self._name,
                      "information": self._information.serialize(),
                      "albums": [album.serialize() for album in self._albums],
                      "friends": [friend.serialize() for friend in self._friends]}
        return serialized

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]) -> "Profile":
        profile = Profile(username=serialized["username"])
        profile._name = serialized["name"]
        profile._information = Information.deserialize(serialized["information"])
        profile._albums = [Album.deserialize(album) for album in serialized["albums"]]
        profile._friends = [Profile.deserialize(friend) for friend in serialized["friends"]]

    def _parse_album_links(self) -> Dict[str, str]:
        return []  # todo: implement

    def _parse_friend_usernames(self) -> List[str]:
        return []  # todo: implement

    def _parse_name(self):
        self._name = self._driver.scrape_text(NAME_XPATH)
