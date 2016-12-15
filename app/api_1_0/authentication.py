from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from .errors import unauthorized, forbidden
from ..models import AnonymousUser, User
from . import api

auth = HTTPBasicAuth()


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.cofirmed:
        return forbidden('Unconfirmed account')


@auth.verify_password
def verify(email, password):
    if email == '':
        g.current_user = AnonymousUser()
        return True
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.route('/token')
def get_token():
    pass

