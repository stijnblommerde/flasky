from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from .errors import unauthorized, forbidden
from ..models import AnonymousUser, User
from . import api

auth = HTTPBasicAuth()


@api.before_request
@auth.login_required
def before_request():
    """ protect all endpoints from logging in anonymously or unconfirmed
    :return:
    """
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@auth.verify_password
def verify_password(email_or_token, password):
    """ callback for flask_httpauth, called after @auth.login_required
    """
    # login anonymously (without email, password or token)
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    # login with token
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.route('/token')
def get_token():
    print('token used:', g.token_used)
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    print('token:',g.current_user.generate_auth_token(expiration=3600))
    print('type:', type(g.current_user.generate_auth_token(expiration=3600)))
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})

