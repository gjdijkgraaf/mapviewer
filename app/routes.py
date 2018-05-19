#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, url_for, jsonify
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Gerrit Jan'}
    return render_template('index.html', title='Home', user=user)

@app.route('/test')
def test():
    user = {'username': 'Gerrit Jan'}
    shape = 'data/provincie_hoofdsteden.geojson'
    return render_template('test.html', title='Test', user=user, shape=shape)

@app.route('/fetch/<layer>', methods=['GET', 'POST'])
def fetch(layer):
    data = {1: {'type': 'Feature',
                'geometry': {'type': 'Point',
                             'coordinates': [6.1, 52.516667]},
                'properties': {'Hoofdstad': 'Zwolle',
                               'Provincie': 'Overijssel'}},
            2: {'type': 'Feature',
                'geometry': {'type': 'Point',
                             "coordinates": [5.916667, 51.983333]},
                'properties': {'Hoofdstad': 'Arnhem',
                               'Provincie': 'Gelderland'}}}
    
    return jsonify(data[int(layer)])

# 1: write functionality to load data on zoom/move 
# 2: write functionality to load data from database based on #1
# 3: write functionality for different projections
# 4: support for users/projects
# 5: admin
    