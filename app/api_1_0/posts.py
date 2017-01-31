from flask import jsonify

from ..models import Post
from .authentication import auth
from . import api


@api.route('/posts/')
@auth.login_required
def get_posts():
    print('enter get_posts')
    posts = Post.query.all()
    return jsonify({'posts': [post.to_json() for post in posts]})


@api.route('/post/<int:id>')
@auth.login_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({'post': post.to_json()})