#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, url_for, jsonify
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    user = {'username': 'Gerrit Jan'}
    return render_template('index.html', title='Home', user=user)

@bp.route('/test')
def test():
    user = {'username': 'Gerrit Jan'}
    shape = 'data/provincie_hoofdsteden.geojson'
    return render_template('test.html', title='Test', user=user, shape=shape)

# 2: write functionality to load data from database based on #1
# 3: write functionality for different projections
# 4: support for users/projects
# 5: admin
