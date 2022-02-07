from sqlalchemy import select

from models import User, Section
from app import db


class BaseCommand(object):
    command = None
    person = None

    def __init__(self, command, person):
        self.command = command
        self.person = person

    def process(self):
        raise Exception('Not implemented')


class RegisterUserCommand(BaseCommand):
    def process(self):
        cmd = self.command.replace('/register_user', '')
        name, class_id = cmd.split(":")
        telegram_id = self.person["id"]
        telegram_name = self.person["username"]
        new_user = User(
            name=name.strip(),
            class_id=class_id.strip(),
            role=1,
            telegram_id=telegram_id,
            telegram_name=telegram_name
        )
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


def get_command_processor(message):
    command = str(message["text"])
    person = message["from"]
    person_role = get_person_role(person)
    person_commands = get_person_commands(person_role)
    if command.startswith('/help'):
        return HelpCommand(command, person)
    elif command.startswith('/register_user'):
        return RegisterUserCommand(command, person)
    elif command.startswith('/list_users'):
        return ListUsersCommand(command, person)
    else:
        return DummyCommand(command, person)


def get_person_role(person):
    # stmt = select(User.role).where(User.telegram_id == person["id"])
    # result = db.session.execute(stmt)
    users = User.query.filter_by(telegram_id=person["id"]).all()
    print('users', users)
    role = max((u.role for u in users), default=1)
    print('role: ', role)
    return role


def get_person_commands(role):
    pass
