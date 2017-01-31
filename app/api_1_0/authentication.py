from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from .errors import unauthorized, forbidden
from ..models import AnonymousUser, User
from . import api

print('test authentication v2')

auth = HTTPBasicAuth()


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@auth.verify_password
def verify(email_or_token, password):
    """
    """
    # possibility to login anonymously
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
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

