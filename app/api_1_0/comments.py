from ..models import Post
from . import api


@api.route('/comments/')
def get_comments():
    pass


@api.route('/post/<int:id>/comments')
def get_post_comments(id):
    post = Post.query.get_or_404(id)
    return post.comments



