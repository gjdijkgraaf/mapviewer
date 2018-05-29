#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, url_for, jsonify
from app import db
from app.models import Project
from app.main import bp

@bp.route('/')
@bp.route('/map')
def index():
    user = {'username': 'Gerrit Jan'}
    return render_template('map.html', title='Home', user=user)

@bp.route('/projects')
def projects():
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    projects = Project.query.all()
    return render_template('projects.html', title='Projects', user=user)
