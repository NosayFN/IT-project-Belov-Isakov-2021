from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import requests

from utils.config import Config

conf = Config.get_instance()
app = Flask(__name__)
app.config.from_object(conf)
db = SQLAlchemy(app)

from utils.message import parse_request


@app.route('/')
def hello_world():
    return "Hello World! I am a test bot"


@app.route('/message', methods=["GET", "POST"])
def message():
    if request.method == "POST":
        msg = parse_request(request.json)
        reply = msg.get_reply()
        if reply is not None:
            send_reply(msg.get_chat_id(), reply)
    return {"ok": True}


def send_reply(chat_id, text):
    method = "sendMessage"
    url = conf.url + method
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


if __name__ == '__main__':
    app.run()
