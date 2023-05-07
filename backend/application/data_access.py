from application.models import db, User, Post, Follow, Comment, Likes
from application.config import ALLOWED_EXTENSIONS_IMG, ALLOWED_EXTENSIONS_TXT
from application.cache import cache

def allowed_file_img(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMG

def allowed_file_txt(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_TXT

@cache.memoize()
def get_all_users():
    users = User.query.all()
    return users

@cache.memoize()
def get_user_username(username):
    user = User.query.filter_by(username=username).first()
    return user

@cache.memoize()
def get_user_roll(roll):
    user = User.query.filter_by(roll=roll).first()
    return user

@cache.memoize()
def get_posts_all():
    posts = Post.query.order_by(Post.roll.desc()).all()
    return posts

@cache.memoize()
def get_post_roll(roll):
    post = Post.query.filter_by(roll = roll).first()
    return post

@cache.memoize()
def get_comments_post(post_id):
    comments = Comment.query.filter_by(post=post_id).order_by(Comment.roll.desc()).all()
    return comments

@cache.memoize()
def get_posts_author(author):
    posts = Post.query.filter_by(author = author).all()
    return posts

@cache.memoize()
def get_posts_author_desc(author):
    posts = Post.query.filter_by(author = author).order_by(Post.roll.desc()).all()
    return posts

@cache.memoize()
def get_content_all():
    posts = db.session.query(Post, User).filter(Post.author==User.username).order_by(Post.roll.desc()).limit(6).all()
    return posts

@cache.memoize()
def get_content_user(follows):
    posts = db.session.query(Post, User).filter(Post.author==User.username, Post.author.in_(follows)).order_by(Post.roll.desc()).limit(6).all()
    return posts

@cache.memoize()
def get_follows(user):
    follows = Follow.query.filter(Follow.follower == user).all()
    return follows

@cache.memoize()
def get_followers(user):
    followers = Follow.query.filter(Follow.following == user).all()
    return followers

@cache.memoize()
def get_follow_status(follower, following):
    follow = Follow.query.filter(Follow.following == following, Follow.follower == follower).all()
    return {"status": "true"} if len(follow) > 0 else {"status": "false"}

@cache.memoize()
def get_like_status(user, post):
    like = Likes.query.filter_by(user=user, post=post).first()
    return like