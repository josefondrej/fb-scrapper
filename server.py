from flask import Flask, render_template, request

from config import FB_WWW_REGULAR, PIC_SUFFIX, PROFILE_PIC_DIR
from fb_objects.public_event import PublicEvent
from profile_server import ProfileServer

app = Flask(__name__)

event_name = None
public_event = None
profile_server = None


@app.route("/", methods=["GET"])
def home():
    ptr = request.args.get("pointer")
    ignore = request.args.get("ignore")

    if ignore is not None:
        profile_server.update_ignore(ignore)
        profile_server.export_filters()

    logic = {"prev": profile_server.get_prev,
             "next": profile_server.get_next,
             None: profile_server.get_next}

    profile = logic[ptr]()

    link = FB_WWW_REGULAR + profile.username
    keywords = profile_server._get_keywords(profile)
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
                           keywords=keywords)


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
    profile_server = ProfileServer(public_event.all_usernames)

    app.run(debug=True)
