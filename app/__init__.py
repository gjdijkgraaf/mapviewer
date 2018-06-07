#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.data import bp as data_bp
    app.register_blueprint(data_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app

from app import models
