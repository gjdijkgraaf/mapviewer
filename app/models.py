from flask import current_app
from app import db

users2projects = db.Table('users2projects',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    displayname = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Layer(db.Model):
    layer_id = db.Column(db.Integer, primary_key=True)
    tablename = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    type = db.Column(db.String(20))

    def __repr__(self):
        return '<Layer {}>'.format(self.name)

class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    users = db.relationship('User', secondary=users2projects, lazy='subquery',
        backref=db.backref('projects', lazy=True))
    layerviews = db.relationship('Layerview', backref='project', lazy=True)

    def __repr__(self):
        return '<Project {}>'.format(self.name)

class Layerview(db.Model):
    layerview_id = db.Column(db.Integer, primary_key=True)
    layer_id = db.Column(db.Integer, db.ForeignKey('layer.layer_id'),
        nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'),
        nullable=False)
    description = db.Column(db.String(256))
    pointtolayer = db.Column(db.String(256))
    style = db.Column(db.String(256))
    oneachfeature = db.Column(db.String(256))

    def __repr__(self):
        return '<Layerview {}>'.format(self.description)
