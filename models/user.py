import sqlite3
from db import db

# (db.Model) will create the mapping between the database and those objects
class UserModel(db.Model):
    #create the tabel for the db:
    __tablename__ = 'users'

    # also telling what colons we want the table to contain:
    id = db.Column(db.Integer, primary_key=True)   # Primary - meaning this is unique
    username = db.Column(db.String(80))   # 80 will limit the size of the username
    password = db.Column(db.String(80))


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        # first username is the table's name and then the argof this method:
        return cls.query.filter_by(username=username).first()


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
