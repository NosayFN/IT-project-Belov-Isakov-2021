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

