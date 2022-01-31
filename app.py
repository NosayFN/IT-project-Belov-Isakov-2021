from flask import Flask, request
import requests
import time

from utils import Config

app = Flask(__name__)

conf = Config.get_instance()


@app.route('/')
def hello_world():
    return "Hello World! I am a test bot"


@app.route('/message', methods=["GET", "POST"])
def message():
    if request.method == "POST":
        print("got request:", request.json)
        msg = request.json.get("message", None)
        if msg is None:
            return {"ok": True}
        chat = msg.get("chat", None)
        if chat is None:
            return {"ok": True}
        chat_id = chat.get("id", None)
        text = msg.get("text", "None")
        send_reply(chat_id, "And now " + request.json["message"]["from"]["username"] +
                   " is asking for " + text +
                   " at " + time.strftime("%D %H:%M", time.localtime(int(request.json["message"]["date"]))))
    return {"ok": True}


def send_reply(chat_id, text):
    method = "sendMessage"
    url = conf.url + method
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


if __name__ == '__main__':
    app.run()
