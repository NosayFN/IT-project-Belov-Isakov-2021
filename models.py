from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    class_id = db.Column(db.String())

    def __repr__(self):
        return '<id: {}, class {}, name: {}>'.\
            format(self.id, self.class_id, self.name)


class Section(db.Model):
    __tablename__ = 'section'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    leader = db.Column(db.String())

    def __init__(self, name, leader):
        self.name = name
        self.leader = leader

    def __repr__(self):
        return '<id: {}, name: {}, leader: {}>'.\
            format(self.id, self.name, self.leader)
