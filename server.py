from flask import Flask, render_template

from fb_objects.profile import Profile
from fb_objects.public_event import PublicEvent
from profile_server import ProfileServer

app = Flask(__name__)

event_name = "some_event"
public_event = PublicEvent.load(event_name)

profile_server = ProfileServer(public_event.all_usernames)


@app.route("/")
def home():
    profile = profile_server.get_next()
    link = "https://facebook.com/" + profile.username
    img_path = "./static/profile_pics/" + profile.username + ".jpg"
    return render_template("main.html", name=profile.name, username=profile.username, link=link, img_path=img_path)


if __name__ == "__main__":
    app.run(debug=True)
