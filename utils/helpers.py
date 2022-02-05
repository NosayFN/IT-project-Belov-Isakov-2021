from .message import Message, BaseMessage, DummyMessage, AddMemberMessage, RemoveMemberMessage
from .command import DummyCommand, RegisterUserCommand, ListUserCommand


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


def get_command_processor(command):
    if command.startswith('/register_user'):
        return RegisterUserCommand(command)
    elif command.startswith('/list_user'):
        return ListUserCommand(command)
    else:
        return DummyCommand(command)
