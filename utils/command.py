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

    def check_cmd_parameters(self, cmd, count):
        params = cmd.split(":")
        if len(params) != count:
            return "\tNot enough parameters! Given {}, expected {}.".format(len(params), count), None
        if len(list(p for p in params if len(p) == 0)):
            return "\tAll parameters must be set!", None
        return None, params


class RegisterUserCommand(BaseCommand):
    def process(self):
        cmd = self.command.replace('/register_user', '')
        error, params = self.check_cmd_parameters(cmd, 2)
        if error:
            return error
        name = params[0].strip()
        class_id = params[1].strip()
        telegram_id = self.person["id"]
        telegram_name = self.person.get("username", None) or \
            " ".join([self.person.get("first_name", "unknown"), self.person.get("last_name", "unknown")])
        new_user = User(
            name=name,
            class_id=class_id,
            role=1,
            telegram_id=telegram_id,
            telegram_name=telegram_name
        )
        db.session.add(new_user)
        db.session.commit()
        return "\tUser '{}' added!".format(str(new_user))


class AddSectionCommand(BaseCommand):
    def process(self):
        cmd = self.command.replace('/add_section', '')
        error, params = self.check_cmd_parameters(cmd, 2)
        if error:
            return error
        user_id = int(params[0].strip())
        name = params[1].strip()
        user = User.query.filter_by(id=user_id).first()
        if user:
            new_section = Section(
                name=name,
                leader=user.name,
                leader_id=user_id
            )
            db.session.add(new_section)
            db.session.commit()
            return "\tSection '{} ({})' added. Leader is '{}'!".format(new_section.name, new_section.id, user.name)
        else:
            return "\tLeader id '{}' not found!".format(user_id)


class ChangeSectionCommand(BaseCommand):
    def process(self):
        cmd = self.command.replace('/change_section', '')
        error, params = self.check_cmd_parameters(cmd, 3)
        if error:
            return error
        section_id = int(params[0].strip())
        name = params[1].strip()
        leader_id = int(params[2].strip())
        leader = User.query.filter_by(id=leader_id).first()
        section = Section.query.filter_by(id=section_id).first()
        if not leader:
            return "\tLeader id '{}' not found!".format(leader_id)
        if not section:
            return "\tSection id '{}' not found!".format(section_id)
        if not name:
            return "\tName is not set!"

        section.name = name
        section.leader_id = leader.id
        section.leader_name = leader.name
        db.session.commit()
        return "\tSection '{}' changed. New name is '{}', leader is '{}'!".format(section.id, section.name, leader.name)


class RemoveSectionCommand(BaseCommand):
    def process(self):
        cmd = self.command.replace('/remove_section', '')
        error, params = self.check_cmd_parameters(cmd, 1)
        if error:
            return error
        section_id = int(params[0].strip())
        section = Section.query.filter_by(id=section_id).first()
        if not section:
            return "\tSection id '{}' not found!".format(section_id)

        db.session.delete(section)
        db.session.commit()
        return "\tSection '{}' deleted!".format(section_id)


class ListSectionsCommand(BaseCommand):
    person_role = 0

    def __init__(self, command, person, person_role):
        super().__init__(command, person)
        self.person_role = person_role

    def process(self):
        sections = Section.query.all()
        return "\tList of sections:\n\t\t" + "\n\t\t".join(section.get_str(self.person_role) for section in sections)


class SetUserRoleCommand(BaseCommand):
    def process(self):
        cmd = self.command.replace('/set_user_role', '')
        error, params = self.check_cmd_parameters(cmd, 2)
        if error:
            return error
        user_id = int(params[0].strip())
        role = params[1].strip()
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
            "/add_section": " [id]:[name], where id is leader id",
            "/change_section": " [id]:[name]:[leader_id], where id is section id",
            "/remove_section": " [id], where id is section id",
            "/set_user_role": " [id]:[role], where id is user id, role is one of the following: <{}>".
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
    elif is_command_allowed(command, '/add_section', person_commands):
        return AddSectionCommand(command, person)
    elif is_command_allowed(command, '/remove_section', person_commands):
        return RemoveSectionCommand(command, person)
    elif is_command_allowed(command, '/change_section', person_commands):
        return ChangeSectionCommand(command, person)
    elif is_command_allowed(command, '/list_sections', person_commands):
        return ListSectionsCommand(command, person, person_role)
    else:
        return DummyCommand(command, person)


def get_person_role(person):
    users = User.query.filter_by(telegram_id=str(person["id"])).all()
    role = max((u.role for u in users), default=0)
    print('role:', Roles(role).name)
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
            "/change_section",
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
