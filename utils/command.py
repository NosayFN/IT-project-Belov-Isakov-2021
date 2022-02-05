from models import User, Section
from app import db


class BaseCommand(object):
    command = None

    def __init__(self, command):
        self.command = command

    def process(self):
        raise Exception('Not implemented')


class RegisterUserCommand(BaseCommand):
    def process(self):
        cmd = self.command.replace('/register_user', '')
        name, class_id = cmd.split(":")
        new_user = User(name=name.strip(), class_id=class_id.strip())
        db.session.add(new_user)
        db.session.commit()
        return "\tUser '" + str(new_user) + "' added!"


class ListUsersCommand(BaseCommand):
    def process(self):
        users = User.query.all()
        return "\tList of registered users:\n\t\t" + "\n\t\t".join(str(user) for user in users)


class HelpCommand(BaseCommand):
    def process(self):
        help_command = \
            "\tList of available commands:\n" \
            "\t\t/help\n" \
            "\t\t/register_user [name]:[class]\n" \
            "\t\t/list_users\n"
        return help_command


class DummyCommand(BaseCommand):
    def process(self):
        return "Unknown command. Type /help to get commands list."


def get_command_processor(command):
    if command.startswith('/help'):
        return HelpCommand(command)
    elif command.startswith('/register_user'):
        return RegisterUserCommand(command)
    elif command.startswith('/list_users'):
        return ListUsersCommand(command)
    else:
        return DummyCommand(command)
