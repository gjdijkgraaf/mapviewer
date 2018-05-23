#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, current_app
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.data import bp as data_bp
    app.register_blueprint(data_bp)

    return app
