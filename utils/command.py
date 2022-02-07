from models import User, Section
from enums import Roles
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
        return "\tUser '{}' added!".format(str(new_user))


class SetUserRoleCommand(BaseCommand):
    def process(self):
        cmd = self.command.replace('/set_user_role', '')
        user_id, role = cmd.split(":")
        user_id = int(user_id.strip())
        role = role.strip()
        if role not in [r.name for r in Roles]:
            return "\tRole '{}' does not exist!".format(role)
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.role = Roles[role].value
            db.session.commit()
            return "\tUser '{} ({})' updated with new role '{}'!".format(user.name, user.id, role)
        else:
            return "\tUser '{}' not found!".format(user_id)


class ListUsersCommand(BaseCommand):
    person_role = 0

    def __init__(self, command, person, person_role):
        super().__init__(command, person)
        self.person_role = person_role

    def process(self):
        users = User.query.all()
        return "\tList of registered users:\n\t\t" + "\n\t\t".join(user.get_str(self.person_role) for user in users)


class HelpCommand(BaseCommand):
    person_commands = []

    def __init__(self, command, person, person_commands):
        super().__init__(command, person)
        self.person_commands = person_commands

    def process(self):
        help_command = ["\tList of available commands:"]
        for command in self.person_commands:
            help_command.append("\t\t" + command + self.inline_help(command))
        return "\n".join(help_command)

    @classmethod
    def inline_help(cls, command):
        return {
            "/register_user": " [name]:[class]",
            "/set_user_role": " [id]:[role], where role is one of the following: <{}>".
                              format(", ".join([r.name for r in Roles])),
        }.get(command, "")


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
        return ListUsersCommand(command, person, person_role)
    elif is_command_allowed(command, '/set_user_role', person_commands):
        return SetUserRoleCommand(command, person)
    else:
        return DummyCommand(command, person)


def get_person_role(person):
    users = User.query.filter_by(telegram_id=str(person["id"])).all()
    role = max((u.role for u in users), default=0)
    print('role:', Roles[role].name)
    return role


def get_person_commands(role):
    # guest commands (role == 0)
    commands = [
        "/help",
        "/register_user",
    ]
    # user commands (role == 1)
    if role >= 1:
        commands.append(
            "/list_users",
        )
    # superuser commands (role == 2)
    if 1 < role <= 7:
        commands.extend([
            "/list_sections",
            "/add_section",
            "/remove_section",
        ])
    # admin commands (role == 7)
    if role == 7:
        commands.extend([
            "/set_user_role",
        ])
    return commands


def is_command_allowed(command, prefix, person_commands):
    if command.startswith(prefix) and prefix in person_commands:
        return True
    return False
