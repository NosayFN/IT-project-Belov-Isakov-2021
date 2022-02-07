from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    class_id = db.Column(db.String())
    role = db.Column(db.Integer(), default=1, server_default="1", nullable=False)
    telegram_id = db.Column(db.String())
    telegram_name = db.Column(db.String())

    def __repr__(self):
        return '<id: {}, name: {}, class: {}, added by: {}>'.\
            format(self.id, self.name, self.class_id, self.telegram_name)

    def __str__(self):
        return 'name: {}, class: {}, added by: {}'.\
            format(self.name, self.class_id, self.telegram_name)


class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    leader = db.Column(db.String())

    def __repr__(self):
        return '<id: {}, name: {}, leader: {}>'.\
            format(self.id, self.name, self.leader)
