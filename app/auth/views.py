import flask
from flask import render_template
from flask_login import login_user

from app.auth.forms import LoginForm
from app.models import User
from . import auth


# url_prefix /auth (app/__init__.py)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(0)
    if form.validate_on_submit():
        # Login and validate the user.
        user = User.query.filter_by(email=form.email.data).first()
        print(1)
        if user is not None and user.verify_password(form.email.data):
            print(2)
            login_user(user, form.remember_me.data)
            print(flask.request.args.get('next'))
            return flask.redirect(flask.request.args.get('next') or
                                  flask.url_for('main.index'))
        flask.flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)