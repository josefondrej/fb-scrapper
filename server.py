from flask import Flask, render_template

from config import FB_WWW_REGULAR, PIC_SUFFIX, PROFILE_PIC_DIR
from fb_objects.public_event import PublicEvent
from profile_server import ProfileServer

app = Flask(__name__)

event_name = None
public_event = None
profile_server = None


@app.route("/")
def home():
    profile = profile_server.get_next()
    link = FB_WWW_REGULAR + profile.username
    img_path = PROFILE_PIC_DIR + profile.username + PIC_SUFFIX
    return render_template("main.html", name=profile.name, username=profile.username, link=link, img_path=img_path)


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
