from flask import render_template, redirect, url_for, request, flash, \
    current_app
from flask_login import login_required, login_user, logout_user, current_user

from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from . import auth
from ..email import send_email


# url prefixed with /auth (url_prefix app/__init__.py)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.email.data):
            login_user(user, form.remember_me.data)
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
        token = user.generate_confirmation_token()
        send_email(current_app.config.get('MAIL_TO') or user.email,
                   'Confirm Your Account',
                   'auth/email/confirm',
                   user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account.')
    else:
        flash('The confirmation link is invalid or expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    """ before request hook
    User is registered and logged in, but cannot access app yet because
    email needs to be confirmed.
    :return:
    """
    if current_user.is_authenticated \
        and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    """ Explain user how to confirm email
    :return:
    """
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_app.config.get('MAIL_TO') or current_user.email,
               'Confirm Your Account',
               'auth/email/confirm',
               user=current_user, token=token)
    flash('A confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))