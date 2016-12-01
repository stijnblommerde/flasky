from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from . import auth


# url prefixed with /auth (url_prefix app/__init__.py)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.email.data):
            login_user(user, form.remember_me.data)
            print(request.args.get('next'))
            return redirect(request.args.get('next') or
                            url_for('main.index'))
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # store user in database
        user = User(username=form.username.data, email=form.email.data,
                    password=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
