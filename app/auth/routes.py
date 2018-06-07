from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    if current_user.is_authenticated:
        return redirect(url_for('main.projects'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.projects')
        flash('Welcome back, {}!'.format(current_user.username))
        return redirect(next_page)
    return render_template('auth/login.html', title="Sign in", form=form, user=user)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#%%-----------------------------------------------------------------------------

@bp.route('/user_overview')
def user_overview():
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    users = User.query.all()
    return render_template('auth/user_overview.html', title="User overview", user=user, users=users)


@bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                    displayname=form.displayname.data,
                    role=form.role.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User created.')
        return redirect(url_for('auth.user_overview'))
    return render_template('auth/add_user.html', title="Add user", user=user, form=form)


@bp.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = {'username': 'Gerrit Jan', 'role': 'admin'}
    edit_user = User.query.get(user_id)
    form = RegistrationForm(obj=edit_user)
    if form.validate_on_submit():
        form.populate_obj(edit_user)
        db.session.commit()
        flash('User updated.')
        return redirect(url_for('auth.user_overview'))
    return render_template('auth/edit_user.html', title="Edit user", form=form, user=user, edit_user=edit_user)
