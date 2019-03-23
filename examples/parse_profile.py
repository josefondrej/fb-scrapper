from fb_objects.profile import Profile
from utils import get_driver


def parse_profile(username: str) -> Profile:
    driver = get_driver()

    profile = Profile(username=username, driver=driver)
    profile.parse()

    driver.close()

    profile.save()
    profile = Profile.load(username)

    return profile


def argparse() -> str:
    import argparse

    parser = argparse.ArgumentParser(description="Parse profile of single person")
    parser.add_argument("--username", help="Person's username")

    args = parser.parse_args()

    username = args.username

    return username


if __name__ == "__main__":
    username = argparse()
    parse_profile(username)
