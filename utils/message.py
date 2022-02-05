import time
from utils.command import get_command_processor


class DummyMessage(object):
    _message = None

    def __init__(self, json):
        pass

    def get_reply(self):
        return None


class BaseMessage(DummyMessage):
    def __init__(self, json):
        super().__init__(json)
        self._message = json["message"]

    def _get_header(self):
        return self._message["from"]["username"] + " "

    def _get_footer(self):
        return " at " + time.strftime("%D %H:%M", time.localtime(int(self._message["date"]))) + "."

    def get_reply(self):
        return self._get_header() + \
               "sent something unexpected" + \
               self._get_footer()

    def get_chat_id(self):
        return self._message["chat"]["id"]


class AddMemberMessage(BaseMessage):
    def get_reply(self):
        return self._get_header() + \
               "added member " + self._message["new_chat_member"].get("username", "Unknown") + \
               self._get_footer()


class RemoveMemberMessage(BaseMessage):
    def get_reply(self):
        return self._get_header() + \
               "removed member " + self._message["left_chat_member"].get("username", "Unknown") + \
               self._get_footer()


class Message(BaseMessage):
    def get_reply(self):
        return self._get_header() + \
               "is asking for " + self._message["text"] + \
               self._get_footer() + "\nResult:\n" + \
               self.process_command()

    def process_command(self):
        command = str(self._message["text"])
        if command.startswith('/'):
            command_processor = get_command_processor(command)
            return command_processor.process()
        else:
            return ""


def parse_request(json):
    print("got request:", json)

    if json.get("message", None) is not None:
        if json["message"].get("text", None) is not None:
            return Message(json)
        elif json["message"].get("new_chat_member", None) is not None:
            return AddMemberMessage(json)
        elif json["message"].get("left_chat_member", None) is not None:
            return RemoveMemberMessage(json)
        else:
            # unexpected (or not supported yet?) message type, f.e. sticker
            return BaseMessage(json)
    else:
        # unexpected message structure
        # possibly some technical message?
        return DummyMessage(json)
