#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, url_for, jsonify, flash, redirect
from app import db
from app.models import Project, User, Layer, Layerview
from app.main import bp
from app.main.forms import AddProjectForm, LayerForm

@bp.route('/')
@bp.route('/map')
def index():
    user = {'username': 'Gerrit Jan'}
    return render_template('map.html', title='Home', user=user)

#%%-----------------------------------------------------------------------------

@bp.route('/projects')
def projects():
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    projects = Project.query.all()
    return render_template('main/projects.html', title='Projects', projects=projects, user=user)

@bp.route('/add_project', methods=['GET', 'POST'])
def add_project():
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    form = AddProjectForm()
    form.users.choices = [(u.user_id, u.username) for u in User.query.order_by('username')]
    form.layers.choices = [(l.layer_id, l.tablename) for l in Layer.query.order_by('layer_id')]
    if form.validate_on_submit():
        layers = form.layers.data
        flash(layers)
        return redirect(url_for('main.projects'))
    return render_template('main/add_project.html', title="Add a project", form=form, user=user)

@bp.route('/edit_project/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    pass

#%%-----------------------------------------------------------------------------

@bp.route('/layers')
def layers():
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    layers = Layer.query.all()
    return render_template('main/layers.html', title='Layers', layers=layers, user=user)

@bp.route('/add_layer', methods=['GET', 'POST'])
def add_layer():
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    form = LayerForm()
    if form.validate_on_submit():
        layer = Layer(tablename=form.tablename.data,
                      description=form.description.data,
                      type=form.type.data)
        db.session.add(layer)
        db.session.commit()
        flash('Layer added.')
        return redirect(url_for('main.layers'))
    return render_template('main/add_layer.html', title="Add a project", form=form, user=user)

@bp.route('/edit_layer/<layer_id>', methods=['GET', 'POST'])
def edit_layer(layer_id):
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    layer = Layer.query.get(layer_id)
    form = LayerForm(obj=layer)
    if form.validate_on_submit():
        form.populate_obj(layer)
        flash('Layer updated.')
        return redirect(url_for('main.layers'))
    return render_template('main/edit_layer.html', title="Edit a layer", layer_id=layer_id, form=form, user=user)
