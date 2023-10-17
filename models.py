from flask_login import UserMixin

from main import db


class Users(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(16))


class LinodeToken(db.Model):
    __tablename__ = 'linode_token'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    token_key = db.Column(db.String(50))
    add_date = db.Column(db.String(10))
    sum = db.Column(db.Integer)
    status = db.Column(db.String(10))
    label = db.Column(db.String(50))


class LinodeServer(db.Model):
    __tablename__ = 'linode_server'
    linode_id = db.Column(db.Integer, primary_key=True)
    ipv4 = db.Column(db.String(15))
    ipv6 = db.Column(db.String(50))
    type = db.Column(db.String(30))
    region = db.Column(db.String(30))
    token_id = db.Column(db.Integer)
    label = db.Column(db.String(50))