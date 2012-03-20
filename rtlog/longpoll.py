import sys

from gevent import monkey
from gevent.event import Event
from gevent.wsgi import WSGIServer

from flask import Flask, jsonify, render_template, request

monkey.patch_socket()

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

class Room(object):
    def __init__(self, n_msg = 20):
        self.messages = []
        self.n_msg = n_msg
        self.event = Event()

    def add_message(self, message):

        self.messages.append(message)
        if len(self.messages) > self.n_msg:
            self.messages.pop(0)
        self.event.set()
        self.event.clear()

    def wait(self):
        self.event.wait()

    def get_messages(self):
        return self.messages

room = Room()
room_freenode = {
    "gevent":Room(),
    "django":Room(),
    "go-nuts":Room(),
    "pocoo":Room(),
    "ibk_test":Room(),
    "rtchatlog":Room(),
    "python":Room(),
    "diesel":Room(),
}

@app.route("/")
def index():
    """
    Display the page containing chat room
    """
    return render_template("index.html")

@app.route("/rtview/<server>/<chan>/")
def rt_view(server, chan):
    if server == "irc.freenode.net":
        chan_room = room_freenode[chan]
        poll_url = "/update_chan/" + server + "/" + chan + "/"
        return render_template("chan.html", messages=chan_room.get_messages(),
                               channel = chan,
                               server = server,
                               poll_url =poll_url)
    
    return "not found"

@app.route("/new_msg_chan/<server>/<chan>/", methods = ["POST"])
def new_msg_chan(server, chan):
    print "new_msg_chan baru = ", chan
    body = request.form['body'].strip()
    
    if server == "irc.freenode.net":
        chan_room = room_freenode[chan]
        if body:
            chan_room.add_message(body)
        return jsonify(success=True)
    else:
        return jsonify(success=False, reason = "unknown channel")

@app.route("/update_chan/<server>/<chan>/", methods=("POST",))
def update_chan(server, chan):
    if server == "irc.freenode.net":
        chan_room = room_freenode[chan]
        chan_room.wait()
        return jsonify(messages=chan_room.get_messages())
    
    return "???"

if __name__ == "__main__":
    WSGIServer(('127.0.0.1', 8080), app.wsgi_app).serve_forever()
