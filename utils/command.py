from models import User, Section
from app import db


class BaseCommand(object):
    command = None

    def __init__(self, command):
        self.command = command

    def process(self):
        raise Exception('Not implemented')


class RegisterUserCommand(BaseCommand):
    pass


class ListUserCommand(BaseCommand):
    def process(self):
        users = User.query.all()
        return "List of registered users:" + users


class HelpCommand(BaseCommand):
    def process(self):
        help_command = \
            "List of available commands:\n" \
            "\t/help\n" \
            "\t/register_user [name] [class]\n" \
            "\t/list_user\n"
        return help_command


class DummyCommand(BaseCommand):
    def process(self):
        return "Unknown command. Type /help to get commands list."


def get_command_processor(command):
    if command.startswith('/help'):
        return HelpCommand(command)
    elif command.startswith('/register_user'):
        return RegisterUserCommand(command)
    elif command.startswith('/list_user'):
        return ListUserCommand(command)
    else:
        return DummyCommand(command)
