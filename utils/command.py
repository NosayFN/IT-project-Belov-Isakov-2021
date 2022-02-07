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
    person_commands = []

    def __init__(self, command, person, person_commands):
        super().__init__(command, person)
        self.person_commands = person_commands

    def process(self):
        help_command = "\tList of available commands:\n"
        for command in self.person_commands:
            help_command += "\t\t" + command + self.inline_help(command)
        return help_command

    @classmethod
    def inline_help(cls, command):
        return {
            '/register_user': " [name]:[class]\n"
        }.get(command, "\n")


class DummyCommand(BaseCommand):
    def process(self):
        return "Unknown command. Type /help to get commands list."


def get_command_processor(message):
    command = str(message["text"])
    person = message["from"]
    person_role = get_person_role(person)
    person_commands = get_person_commands(person_role)
    if command.startswith('/help'):
        return HelpCommand(command, person, person_commands)
    elif is_command_allowed(command, '/register_user', person_commands):
        return RegisterUserCommand(command, person)
    elif is_command_allowed(command, '/list_users', person_commands):
        return ListUsersCommand(command, person)
    else:
        return DummyCommand(command, person)


def get_person_role(person):
    users = User.query.filter_by(telegram_id=str(person["id"])).all()
    role = max((u.role for u in users), default=0)
    print('role: ', role)
    return role


def get_person_commands(role):
    # guest commands
    commands = [
        "/help",
        "/register_user",
    ]
    # user commands
    if role == 1:
        commands.append([
            "/list_users",
        ])
    # superuser commands
    if 1 < role < 7:
        commands.append([
            "/list_sections",
            "/add_section",
            "/remove_section",
        ])
    # admin commands
    if role == 7:
        commands.append([
            "/set_user_role",
        ])
    return commands


def is_command_allowed(command, prefix, person_commands):
    if command.startswith(prefix) and prefix in person_commands:
        return True
    return False
