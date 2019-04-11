from typing import List, Dict, Any

from fb_objects.annotation import Annotation
from utils import parse_usernames
from config import FB_WWW, INFORMATION_SUFFIX, ALBUMS_SUFFIX, FRIENDS_SUFFIX, NAME_XPATH, PROFILE_PIC_XPATH, \
    PROFILE_PIC_DIR, PIC_SUFFIX, FRIEND_USERNAME_XPATH, NEXT_FRIENDS_XPATH, \
    MAIN_PAGE_SUFFIX, PROFILE_DIR, PROFILE_SUFFIX, LARGE_PROFILE_PIC_XPATH, FB_WWW_REGULAR, PROFILE_PIC_XPATH_ANONYMOUS
from fb_objects.fb_object import FbObject
from fb_objects.information import Information
from fb_objects.album import Album
from webdriver_wrapper import WebDriverWrapper


class Profile(FbObject):
    _file_dir = PROFILE_DIR
    _file_suffix = PROFILE_SUFFIX
    _file_name_key = "_username"

    def __init__(self, username: str, driver: WebDriverWrapper = None):
        super().__init__(driver)
        self._username: str = username
        self._name: str = None
        self._information: Information = None
        self._albums: List[Album] = None
        self._friends: List[str] = None
        self._annotation: Annotation = None

    @property
    def name(self):
        return self._name

    @property
    def username(self):
        return self._username

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
        self._point_driver_to(MAIN_PAGE_SUFFIX)
        self._name = self._parse_name()
        self._download_profile_picture()

        self._point_driver_to(INFORMATION_SUFFIX)
        self._information = Information(self._driver).parse()

        self._point_driver_to(ALBUMS_SUFFIX)
        self._parse_albums()

        self._point_driver_to(FRIENDS_SUFFIX)
        self._friends = self._parse_friend_usernames()

        return self

    def _parse_information(self):
        self._point_driver_to(INFORMATION_SUFFIX)
        self._information = Information(self._driver).parse()

    def serialize(self) -> Dict[str, Any]:
        serialized = {"username": self._username,
                      "name": self._name,
                      "information": FbObject._magic_serialize(self._information),
                      "albums": FbObject._magic_serialize(self._albums),
                      "friends": self._friends,
                      "annotation": FbObject._magic_serialize(self._annotation)}

        return serialized

    @classmethod
    def deserialize(cls, serialized: Dict[str, Any]) -> "Profile":
        profile = Profile(username=serialized["username"])

        profile._name = serialized["name"]
        profile._information = FbObject._magic_deserialize(serialized["information"], Information)
        profile._albums = FbObject._magic_deserialize(serialized["albums"], Album)
        profile._friends = serialized["friends"]
        profile._annotation = Annotation.deserialize(serialized.get("annotation"))

        return profile

    def annotate(self, value: int = 0):
        if self._annotation is None:
            self._annotation = Annotation()
        self._annotation._value += value

    def _point_driver_to(self, page_suffix: str):
        url_albums = FB_WWW + self._username + page_suffix
        self._driver.go_to(url_albums)

    def _parse_albums(self) -> List[Album]:
        albums = []
        album_links = self._parse_album_links()

        for name, link in album_links.items():
            try:
                self._driver.go_to(link)
                album = Album(name=name, driver=self._driver).parse()
                self.albums.append(album)
                self._driver.back()
            except Exception as e:
                print(f"[ERROR] Parsing album ({name}) of ({self._username})")

        return albums

    def _parse_album_links(self) -> Dict[str, str]:
        return {}  # todo: implement

    def _parse_friend_usernames(self) -> List[str]:
        friend_usernames = parse_usernames(FRIEND_USERNAME_XPATH, NEXT_FRIENDS_XPATH, self._driver)
        return friend_usernames

    def _parse_name(self) -> str:
        name = None
        try:
            name = self._driver.scrape_text(NAME_XPATH)
        except Exception as e:
            print(f"[ERROR] Downloading name for ({self._username})")
        return name

    def _download_profile_picture(self):
        try:
            self._driver.click(PROFILE_PIC_XPATH)

            profile_pic_path = PROFILE_PIC_DIR + self._username + PIC_SUFFIX
            self._driver.download_image(profile_pic_path, xpath=LARGE_PROFILE_PIC_XPATH)
            self._driver.back()

        except:
            print(f"[ERROR] Downloading profile picture ({self._username})")

    def download_profile_picture_anonymous(self):
        try:
            profile_pic_path = PROFILE_PIC_DIR + self._username + PIC_SUFFIX
            self._driver.go_to(FB_WWW_REGULAR + self._username)
            self._driver.download_image(profile_pic_path, PROFILE_PIC_XPATH_ANONYMOUS)
        except:
            print(f"[ERROR] Downloading profile picture ({self._username})")
