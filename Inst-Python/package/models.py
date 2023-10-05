from datetime import datetime

from flask import url_for
from flask_login import UserMixin

from package import db


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    username = db.Column(db.String(300), nullable=False)
    avatar = db.Column(db.String(300), nullable=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymus(self):
        return False

    def get_id(self):
        return self.id

    def get_login(self):
        return self.login

    def get_username(self):
        return self.username

    def get_avatar(self):
        if self.avatar == 'NULL':
            img = url_for('static', filename='images/default.jpg')
        else:
            img = url_for('static', filename='images/avatar_user/' + str(self.login) + '.jpg')
        return img

    def __repr__(self):
        return '<Users %r>' % self.login

class Image(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Login = db.Column(db.String(50), nullable=True)
    NamePhoto = db.Column(db.String(300), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Image %r>' % self.id