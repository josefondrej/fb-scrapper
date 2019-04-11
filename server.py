from flask import Flask, render_template, request

from config import FB_WWW_REGULAR, PIC_SUFFIX, PROFILE_PIC_DIR
from fb_objects.public_event import PublicEvent
from profile_server import ProfileServer
import utils

app = Flask(__name__)

event_name = None
public_event = None
profile_server = None


@app.route("/", methods=["GET"])
def home():
    ptr = request.args.get("pointer")
    ignore = request.args.get("ignore")
    username = request.args.get("username")
    star = request.args.get("star")

    if ignore is not None:
        profile_server.update_ignore(ignore)
        profile_server.export_filters()

    profile = profile_server.current()

    if star is not None:
        profile_server.current().annotate(1)
    else:
        profile_server.current().annotate(0)
    profile_server.current().save()

    if ptr is not None:
        logic = {"prev": profile_server.get_prev,
                 "next": profile_server.get_next}
        profile = logic[ptr]()

    if username is not None:
        profile = profile_server.get_username(username)

    link = FB_WWW_REGULAR + profile.username
    keywords = profile_server.get_keywords(profile)
    friends_going = profile_server.get_friends_going(profile)
    img_path = PROFILE_PIC_DIR + profile.username + PIC_SUFFIX

    try:
        with open(img_path, "rb"):
            pass
    except IOError:
        img_path = "static/no_image.jpg"

    return render_template("main.html",
                           name=profile.name,
                           username=profile.username,
                           link=link,
                           img_path=img_path,
                           keywords=keywords,
                           friends_going=friends_going)


def argparse() -> str:
    import argparse

    parser = argparse.ArgumentParser(description="Show dashboard for some event")
    parser.add_argument("--event-name", help="Your name for the event", default="some_event")

    args = parser.parse_args()

    event_name = args.event_name

    return event_name


if __name__ == "__main__":
    event_name = argparse()
    public_event = PublicEvent.load(event_name)
    if public_event:
        usernames = public_event.all_usernames
    else:
        usernames = utils.list_usernames()
    profile_server = ProfileServer(usernames)

    app.run(debug=True)
