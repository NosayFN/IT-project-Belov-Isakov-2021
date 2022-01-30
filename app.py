from flask import Flask, request
import requests

from utils import Config

app = Flask(__name__)

conf = Config.get_instance()


@app.route('/')
def hello_world():
    return "Hello World! I am a test bot"


@app.route('/message', methods=["GET", "POST"])
def message():
    if request.method == "POST":
        print(request.json)
        chat_id = request.json["message"]["chat"]["id"]
        send_message(chat_id, "pong")
    return {"ok": True}


def send_message(chat_id, text):
    method = "sendMessage"
    url = conf.url + method
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


if __name__ == '__main__':
    app.run()
