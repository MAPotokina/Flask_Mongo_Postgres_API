from app.init_postgres import db
from app.init_mongodb import mongo
from flask import jsonify


class UserPostgres(db.Model):
    """This class represents the users table."""

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))

    def __init__(self, username, firstname, lastname):
        """initialize with name."""
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return UserPostgres.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User: {} - {} {}>".format(self.username, self.firstname, self.lastname)


class UserMongoDB:

    def __init__(self, username, firstname, lastname):
        """initialize with name."""
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

    def save(self):
        users = mongo.db.users
        users.insert_one({'username': self.username, 'firstname': self.firstname, 'lastname': self.lastname})

    @staticmethod
    def get_all():
        users = mongo.db.users
        output = []
        for q in users.find():
            output.append(UserMongoDB(username=q['username'], firstname=q['firstname'], lastname=q['lastname']))
        return output

    @staticmethod
    def find_by_username(username):
        users = mongo.db.users
        q = users.find_one({'username': username})
        if q:
            return UserMongoDB(username=q['username'], firstname=q['firstname'], lastname=q['lastname'])

    def delete(self):
        users = mongo.db.users
        users.delete_one({'username': self.username})

    def __repr__(self):
        return "<User: {} - {} {}>".format(self.username, self.firstname, self.lastname)
