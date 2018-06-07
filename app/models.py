from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

users2projects = db.Table('users2projects',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    displayname = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Layer(db.Model):
    layer_id = db.Column(db.Integer, primary_key=True)
    tablename = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    geometry_type = db.Column(db.String(20))
    geometry_column = db.Column(db.String(64))
    id_column = db.Column(db.String(64))
    layerviews = db.relationship('Layerview', backref='layer', lazy=True, cascade='delete')

    def __repr__(self):
        return '<Layer {}>'.format(self.tablename)


class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    users = db.relationship('User', secondary=users2projects, lazy='subquery',
        backref=db.backref('projects', lazy=True))
    layerviews = db.relationship('Layerview', backref='project', lazy=True, cascade='delete', order_by='Layerview.order')

    def __repr__(self):
        return '<Project {}>'.format(self.name)


class Layerview(db.Model):
    layerview_id = db.Column(db.Integer, primary_key=True)
    layer_id = db.Column(db.Integer, db.ForeignKey('layer.layer_id'),
        nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'),
        nullable=False)
    name = db.Column(db.String(64))
    order = db.Column(db.Integer)
    description = db.Column(db.String(256))
    pointtolayer = db.Column(db.String(256))
    style = db.Column(db.String(256))
    oneachfeature = db.Column(db.String(256))

    def __repr__(self):
        return '<Layerview {}>'.format(self.description)
