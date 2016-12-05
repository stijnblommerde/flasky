import os

from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, \
    abort
from flask_login import login_required

from app.decorators import admin_required, permission_required
from . import main
from .forms import NameForm, EditProfileForm
from .. import db
from ..models import User, Permission


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'],
                           'New User',
                           'mail/new_user',
                           user=user.username)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time = datetime.utcnow())


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "for administrators!"


@main.route('/moderators')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "for administrators!"


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        return 'valid form'
    return render_template('edit_profile.html', user=user)
