from typing import List, Dict, Any

from config import FB_WWW, INFORMATION_SUFFIX, ALBUMS_SUFFIX, FRIENDS_SUFFIX, NAME_XPATH, PROFILE_PIC_XPATH, \
    SHOW_FULL_SIZE_XPATH, PROFILE_PIC_DIR, PIC_SUFFIX, FRIEND_USERNAME_XPATH, NEXT_FRIENDS_XPATH, FILTERED_USERNAMES
from fb_objects.fb_object import FbObject
from fb_objects.information import Information
from fb_objects.album import Album
from webdriver_wrapper import WebDriverWrapper


class Profile(FbObject):
    def __init__(self, username: str, driver: WebDriverWrapper = None):
        super().__init__(driver)
        self._username: str = username
        self._name: str = None
        self._information: Information = None
        self._albums: List[Album] = None
        self._friends: List[str] = None

    @property
    def information(self) -> Information:
        return self._information

    @property
    def albums(self) -> List[Album]:
        return self._albums

    @property
    def friends(self) -> "List[str]":
        return self._friends

    def parse(self):
        self._point_driver_to_main_page()
        self._parse_name()
        self._download_profile_picture()

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
        self._friends = self._parse_friend_usernames()

        return self

    def serialize(self) -> Dict[str, Any]:
        serialized = {"username": self._username,
                      "name": self._name,
                      "information": FbObject._magic_serialize(self._information),
                      "albums": FbObject._magic_serialize(self._albums),
                      "friends": self._friends}
        return serialized

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]) -> "Profile":
        profile = Profile(username=serialized["username"])
        profile._name = serialized["name"]
        profile._information = FbObject._magic_deserialize(serialized["information"], Information)
        profile._albums = FbObject._magic_deserialize(serialized["albums"], Album)
        profile._friends = serialized["friends"]
        return profile

    def _point_driver_to_main_page(self):
        url_information = FB_WWW + self._username
        self._driver.go_to(url_information)

    def _parse_album_links(self) -> Dict[str, str]:
        return {}  # todo: implement

    def _parse_friend_usernames(self) -> List[str]:
        friend_usernames = []
        while True:
            try:
                friend_elements = self._driver._driver.find_elements_by_xpath(FRIEND_USERNAME_XPATH)
                links = [e.get_attribute("href") for e in friend_elements]
                new_usernames = [self._parse_username_from_link(link) for link in links]
                new_usernames = [username for username in new_usernames if username not in FILTERED_USERNAMES]
                friend_usernames.extend(new_usernames)
                self._driver.click(NEXT_FRIENDS_XPATH)
            except Exception as e:
                return friend_usernames

    def _parse_username_from_link(self, link: str) -> str:
        username = link.split("/")[3].split("?")[0]
        return username

    def _parse_name(self):
        self._name = self._driver.scrape_text(NAME_XPATH)

    def _download_profile_picture(self):
        self._driver.click(PROFILE_PIC_XPATH)
        self._driver.click(SHOW_FULL_SIZE_XPATH)

        if self._driver.focus_on_window(1):
            profile_pic_path = PROFILE_PIC_DIR + self._username + PIC_SUFFIX
            self._driver.download_image(target_file=profile_pic_path)
            self._driver.close_tab()
        self._driver.focus_on_window(0)
