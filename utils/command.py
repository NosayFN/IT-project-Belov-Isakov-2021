from models import User, Section


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
        return "List of registered users:"


class DummyCommand(BaseCommand):
    def process(self):
        return "Unknown command"


def get_command_processor(command):
    if command.startswith('/register_user'):
        return RegisterUserCommand(command)
    elif command.startswith('/list_user'):
        return ListUserCommand(command)
    else:
        return DummyCommand(command)
