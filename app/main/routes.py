#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from flask import render_template, url_for, jsonify, flash, redirect, request
from flask_login import current_user, login_required
from app import db
from app.models import Project, User, Layer, Layerview
from app.main import bp
from app.main.forms import AddProjectForm, EditProjectForm, LayerForm, \
    LayerviewForm, DeleteConfirmationForm, AddLayerviewForm, AddUser2ProjectForm

@bp.route('/index')
def index():
    user = {'username': 'Gerrit Jan'}
    return render_template('map_old.html', title='Home', user=user)

#%%-----------------------------------------------------------------------------

@bp.route('/map/<project_name>')
def map(project_name):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    project = Project.query.filter_by(name=project_name).first_or_404()
    if not current_user in project.users:
        return redirect(url_for('main.projects'))
    return render_template('main/map.html', title=project.name, project=project)


@bp.route('/projects')
def projects():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if current_user.role == 'user':
        projects = db.session.query(Project).join(Project.users).filter(User.id == current_user.id)
    else:
        projects = Project.query.all()
    return render_template('main/projects.html', title='Projects', projects=projects)


@bp.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if current_user.role != 'admin':
        return redirect(url_for('main.projects'))
    form = AddProjectForm()
    form.users.choices = [(u.id, u.username) for u in User.query.order_by('username')]
    form.layers.choices = [(l.layer_id, l.tablename) for l in Layer.query.order_by('layer_id')]
    if form.validate_on_submit():
        check = Project.query.filter_by(name=form.name.data).first()
        if check is not None:
            flash('A project with name "{}" already exists.'.format(form.name.data), 'error')
            return redirect(url_for('main.add_project'))
        else:
            project = Project(name=form.name.data,
                              description=form.description.data)
            db.session.add(project)
            db.session.commit()
            user_ids = form.users.data
            for user_id in user_ids:
                user = User.query.get(user_id)
                project.users.append(user)
                db.session.commit()
            layer_ids = form.layers.data
            for order, layer_id in enumerate(layer_ids):
                layer = Layer.query.get(layer_id)
                layerview = Layerview(layer=layer,
                                      project=project,
                                      name=layer.tablename,
                                      order=order)
                db.session.add(layerview)
                db.session.commit()
            flash('Project {} added.'.format(project.name))
            return redirect(url_for('main.projects'))
    return render_template('main/add_project.html', title="Add a project", form=form)


@bp.route('/edit_project/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.projects'))
    project = Project.query.get(project_id)
    form = EditProjectForm(obj=project)
    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.commit()
        flash('Project updated.')
        return redirect(url_for('main.edit_project', project_id=project_id))
    return render_template('main/edit_project.html', title="Edit project", form=form, project=project)


@bp.route('/add_user_to_project/<project_id>', methods=['GET', 'POST'])
def add_user_to_project(project_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.projects'))
    project = Project.query.get(project_id)
    form = AddUser2ProjectForm()
    form.users.choices = [(u.id, u.username) for u in User.query.order_by('username')]
    if form.validate_on_submit():
        for user_id in form.users.data:
            user = User.query.get(user_id)
            if user in project.users:
                continue
            else:
                project.users.append(user)
                db.session.commit()
        flash('Project users updated.')
        return redirect(url_for('main.edit_project', project_id=project_id))
    return render_template('main/add_user_to_project.html', title="Add user to project", form=form)


@bp.route('/remove_user_from_project/<user_id>', methods=['GET', 'POST'])
def remove_user_from_project(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.projects'))
    project_id = request.args.get('project_id')
    user = User.query.get(user_id)
    project = Project.query.get(project_id)
    form = DeleteConfirmationForm()
    if form.validate_on_submit():
        if form.confirmation.data == 'Yes':
            project.users.remove(user)
            db.session.commit()
            flash('User removed from project.')
        else:
            flash('User removal cancelled.')
        return redirect(url_for('main.edit_project', project_id=project_id))
    return render_template('main/remove_user_from_project.html', form=form, project=project, user=user)


@bp.route('/delete_project/<project_id>', methods=['GET', 'POST'])
def delete_project(project_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.projects'))
    project = Project.query.get(project_id)
    form = DeleteConfirmationForm()
    if form.validate_on_submit():
        if form.confirmation.data == 'Yes':
            db.session.delete(project)
            db.session.commit()
            flash('Project deleted.')
        else:
            flash('Project deletion cancelled.')
        return redirect(url_for('main.projects'))
    return render_template('main/delete_project.html', title="Delete project", form=form, user=user, project=project)

#%%-----------------------------------------------------------------------------

@bp.route('/layers')
def layers():
    if current_user.role != 'admin':
        return redirect(url_for('main.projects'))
    layers = Layer.query.all()
    return render_template('main/layers.html', title='Layers', layers=layers)


@bp.route('/add_layer', methods=['GET', 'POST'])
def add_layer():
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    form = LayerForm()
    data = requests.get(url_for('data.list_tables', _external=True)).json()
    tables = [row[0] for row in data]
    form.tablename.choices = [(name, name) for name in tables]
    if form.validate_on_submit():
        tablename = form.tablename.data
        if Layer.query.filter_by(tablename=tablename).first() is not None:
            flash('A layer with that tablename already exists.')
            return redirect(url_for('main.add_layer'))
        layer = Layer(tablename=form.tablename.data,
                      description=form.description.data,
                      geometry_type=form.geometry_type.data,
                      geometry_column=form.geometry_column.data,
                      id_column=form.id_column.data)
        db.session.add(layer)
        db.session.commit()
        flash('Layer added.')
        return redirect(url_for('main.layers'))
    return render_template('main/add_layer.html', title="Add a layer", form=form, user=user)


@bp.route('/edit_layer/<layer_id>', methods=['GET', 'POST'])
def edit_layer(layer_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.projects'))
    layer = Layer.query.get(layer_id)
    form = LayerForm()
    form.tablename.choices = [(layer.tablename, layer.tablename)]
    if request.method == 'GET':
        form.description.data = layer.description
        form.geometry_type.data = layer.geometry_type
        form.geometry_column.data = layer.geometry_column
        form.id_column.data = layer.id_column
    if form.validate_on_submit():
        layer.tablename = form.tablename.data
        layer.description = form.description.data
        layer.geometry_type = form.geometry_type.data
        layer.geometry_column = form.geometry_column.data
        layer.id_column = form.id_column.data
        db.session.commit()
        flash('Layer updated.')
        return redirect(url_for('main.layers'))
    return render_template('main/edit_layer.html', title="Edit a layer", layer=layer, form=form)


@bp.route('/delete_layer/<layer_id>', methods=['GET', 'POST'])
def delete_layer(layer_id):
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    layer = Layer.query.get(layer_id)
    form = DeleteConfirmationForm()
    if form.validate_on_submit():
        if form.confirmation.data == 'Yes':
            db.session.delete(layer)
            db.session.commit()
            flash('Layer deleted.')
        else:
            flash('Deletion cancelled.')
        return redirect(url_for('main.layers'))
    return render_template('main/delete_layer.html', title="Delete layer", form=form, user=user, layer=layer)


#%%-----------------------------------------------------------------------------

@bp.route('/add_layerview/<project_id>', methods=['GET', 'POST'])
def add_layerview(project_id):
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    project = Project.query.get(project_id)
    layers = Layer.query.all()
    form = AddLayerviewForm()
    form.project.choices = [(project.name, project.name)]
    form.layer.choices = [(layer.tablename, layer.tablename) for layer in layers]
    if form.validate_on_submit():
        layer = Layer.query.filter_by(tablename=form.layer.data).first()
        layerview = Layerview(project=project,
                              layer=layer,
                              name=str(form.name.data),
                              order=form.order.data,
                              description=str(form.description.data),
                              pointtolayer=str(form.pointtolayer.data),
                              style=str(form.style.data),
                              oneachfeature=str(form.oneachfeature.data))
        db.session.add(layerview)
        db.session.commit()
        flash('Layerview created.')
        return redirect(url_for('main.edit_project', project_id=project_id))
    return render_template('main/add_layerview.html', title="Add layerview", form=form, user=user)

@bp.route('/edit_layerview/<layerview_id>', methods=['GET', 'POST'])
def edit_layerview(layerview_id):
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    layerview = Layerview.query.get(layerview_id)
    form = LayerviewForm(obj=layerview)
    if form.validate_on_submit():
        form.populate_obj(layerview)
        db.session.commit()
        flash('Layerview updated.')
        return redirect(url_for('main.edit_project', project_id=layerview.project.project_id))
    return render_template('main/edit_layerview.html', title="Edit layerview", layerview=layerview, form=form, user=user)

@bp.route('/delete_layerview/<layerview_id>', methods=['GET', 'POST'])
def delete_layerview(layerview_id):
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    layerview = Layerview.query.get(layerview_id)
    form = DeleteConfirmationForm()
    if form.validate_on_submit():
        if form.confirmation.data == 'Yes':
            db.session.delete(layerview)
            db.session.commit()
            flash('Project deleted.')
        else:
            flash('Deletion cancelled.')
        return redirect(url_for('main.projects'))
    return render_template('main/delete_layerview.html', title="Delete layerview", form=form, user=user, layerview=layerview)

#%%-----------------------------------------------------------------------------

@bp.route('/fetch_tables')
def fetch_tables():
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    data = requests.get(url_for('data.list_tables', _external=True)).json()
    tables = [row[0] for row in data]
    return render_template('main/test.html', data=tables, user=user)
