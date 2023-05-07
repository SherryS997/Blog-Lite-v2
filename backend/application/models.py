from flask_sqlalchemy import SQLAlchemy
from application.database import db

class User(db.Model):
    __tablename__ = "user"
    roll = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    img = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    posted = db.Column(db.Integer, nullable=False)
    pdf = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "roll": self.roll,
            "username": self.username,
            "email": self.email,
            "img": self.img,
            "posted": self.posted,
            "pdf": self.pdf
        }

class Post(db.Model):
    __tablename__ = "post"
    roll = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String, db.ForeignKey(User.username), nullable=False)
    img = db.Column(db.String)
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.String)
    title = db.Column(db.String, nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "roll": self.roll,
            "title": self.title,
            "text": self.text,
            "author": self.author,
            "img": self.img,
            "date": self.date,
            "likes": self.likes,
        }

class Comment(db.Model):
    __tablename__ = "comment"
    roll = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String, nullable=False)
    post = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "author": self.author,
            "post": self.post,
            "comment": self.comment,
        }

class Follow(db.Model):
    __tablename__ = "follow"
    roll = db.Column(db.Integer, primary_key=True, autoincrement=True)
    following = db.Column(db.Integer, db.ForeignKey(User.roll), nullable=False)
    follower = db.Column(db.Integer, db.ForeignKey(User.roll), nullable=False)

    def to_dict(self):
        return {
            "following": self.following,
            "follower": self.follower,
        }

class Token(db.Model):
    __tablename__ = "token"
    user = db.Column(db.Integer, db.ForeignKey(User.roll), primary_key=True, nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)

class Likes(db.Model):
    __tablename__ = "likes"
    roll = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey(User.roll), nullable=False)
    post = db.Column(db.Integer, db.ForeignKey(Post.roll), nullable=False)
