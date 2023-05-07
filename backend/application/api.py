from flask_restful import Resource, request, reqparse
from application.models import User, Post, Comment, Follow, Token
from application.database import db
from application.validation import BusinessValidationError, NotFoundError, DuplicationError, NotAuthorizedError
from application.config import UPLOAD_FOLDER
from application.data_access import *
from application.cache import cache
from application.utils import convert_to_webp
from passlib.hash import pbkdf2_sha256 as passhash
import secrets
import os, requests, json
import datetime as dt

class UserAPI(Resource):
 
    def get(self, username):
        user = get_user_username(username)
        if user:
            return user.to_dict()
        else:
            raise NotFoundError(404, "User not found")

    def put(self):
        auth = request.headers.get("Authorization", "").split()[1]
        token_id = Token.query.filter_by(token=auth).first()
        if not token_id:
            raise NotAuthorizedError(401, "Invalid or missing token")
        
        user = User.query.filter_by(roll=token_id.user).first()
        if not user:
            raise NotFoundError(404, "User not found")

        if "New Username" in request.form and request.form["New Username"]:
            posts = Post.query.filter_by(author=user.username).all()
            comments = Comment.query.filter_by(author=user.username).all()
            user.username = request.form["New Username"]
            for comment in comments:
                comment.author = request.form["New Username"]
            for post in posts:
                post.author = request.form["New Username"]
        
        if "New Password" in request.form and request.form["New Password"]:
            if len(request.form["New Password"]) < 4:
                raise BusinessValidationError(400, "USER002", "Password should be at least 4 characters long")
            user.password = passhash.hash(request.form["New Password"])

        if "New Email" in request.form and request.form["New Email"]:
            user.email = request.form["New Email"]

        if "New Format" in request.form and request.form["New Format"]:
            user.pdf = int(request.form["New Format"])

        if "New Image" in request.files and request.files["New Image"]:
            file = request.files["New Image"]
            if not allowed_file_img(file.filename):
                raise BusinessValidationError(400, "USER001", "Invalid file type")
            if int(user.img) == 0:
                user.img = str(user.roll)
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER + "Users/", user.img +".webp")
            with open(filepath, 'wb') as f:
                f.write(convert_to_webp(file))

        cache.delete_memoized(get_user_username, user.username)
        cache.delete_memoized(get_user_roll, user.roll)
        db.session.commit()

        return get_user_roll(token_id.user).to_dict()
    
    def delete(self):
        auth = request.headers.get("Authorization", "").split()[1]
        token_id = Token.query.filter_by(token=auth).first()
        if not token_id:
            raise NotAuthorizedError(401, "Invalid or missing token")
        
        user = User.query.filter_by(roll=token_id.user).first()
        if not user:
            raise NotFoundError(404, "User not found")

        resp = requests.get("http://localhost:2345/api/token-jwt", headers=request.headers)
        token = resp.json().get("jwt")
        if not token:
            raise NotAuthorizedError(401, "Invalid or missing token")

        resp = requests.delete("http://localhost:2345/vueapp/user", headers={"Authorization": token})

        return "Successfully Deleted"


    def post(self):
        username = request.form.get("Username")
        password = request.form.get("Password")
        image_file = request.files.get("Image")
        email = request.form.get("Email")

        if not username:
            raise BusinessValidationError(400, "USER003", "Username is required")

        if not email:
            raise BusinessValidationError(400, "USER004", "Email is required")

        if not password or len(password) < 4:
            raise BusinessValidationError(400, "USER002", "Password should be at least 4 characters long")

        if User.query.filter_by(username=username).first():
            raise DuplicationError(409, "Username already exists")

        user = User(username=username, email=email, password=passhash.hash(password), img=0, posted=0, pdf=0)
        db.session.add(user)
        db.session.commit()
        db.session.add(Token(user=user.roll, token=secrets.token_urlsafe(32)))
        db.session.commit()

        if image_file:
            if not allowed_file_img(image_file.filename):
                raise BusinessValidationError(400, "USER001", "Invalid file type")
            if int(user.img) == 0:
                user.img = str(user.roll)
            image_file.save(os.path.join(UPLOAD_FOLDER+"Users/", user.img +".jpg"))
            db.session.commit()

        cache.clear()
        
        return user.to_dict()

class PostAPI(Resource):
    def get(self, post_id):
        post = get_post_roll(post_id)
        if post:
            post.views += 1
            db.session.commit()
            return post.to_dict()
        user = get_user_username(post_id)
        if user:
            posts = get_posts_author(user.username)
            return [post.to_dict() for post in posts]
        else:
            raise NotFoundError(404, "Resource not found")

    def put(self, post_id):
        token = request.headers.get("Authorization")
        if not token:
            raise NotAuthorizedError(401, "No Token Provided")
        token_id = Token.query.filter_by(token=token.split()[1]).first()
        if not token_id:
            raise NotAuthorizedError(401, "Invalid Token")
        user = User.query.filter_by(roll=token_id.user).first()
        if not user:
            raise NotFoundError(404, "User not found")
        
        post = Post.query.filter_by(roll=post_id).first()
        if not post:
            raise NotFoundError(404, "Post not found")

        title = request.form.get("Title", "").strip()
        if title:
            post.title = title
        
        text_file = request.files.get("Text")
        if text_file:
            out = text_file.read().decode('utf8')
            post.text = out
        
        new_image = request.files.get("New Image")
        if new_image:
            if not allowed_file_img(new_image.filename):
                raise BusinessValidationError(400, "POST001", "Invalid file type")
            filepath = os.path.join(UPLOAD_FOLDER+"Posts/", post.img +".webp")
            with open(filepath, 'wb') as f:
                f.write(convert_to_webp(new_image))
        
        db.session.commit()
        cache.clear()

        return post.to_dict()
    
    def delete(self, post_id):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise NotAuthorizedError(401, "No Token Provided")
        
        token = auth_header.split()[1]
        token_id = Token.query.filter_by(token=token).first()
        if not token_id:
            raise NotAuthorizedError(401, "Invalid Token")

        # Use the same token to make a request to another API
        headers = {"Authorization": auth_header}
        resp = requests.get("http://localhost:2345/api/token-jwt", headers=headers)
        new_token = resp.json()["jwt"]
        headers = {"Authorization": new_token}
        resp = requests.delete(f'http://localhost:2345/vueapp/post/{post_id}', headers=headers)

        return "Successfully Deleted"
            
    def post(self):
        token = request.headers.get("Authorization")
        if not token:
            raise NotAuthorizedError(401, "No Token Provided")
        token_id = Token.query.filter_by(token=token.split()[1]).first()

        if not token_id:
            raise NotAuthorizedError(401, "Invalid Token")

        user = User.query.filter_by(roll=token_id.user).first()

        if not user:
            raise NotFoundError(404, "User not found")

        username = user.username

        last_post = Post.query.order_by(Post.roll.desc()).first()
        day = str(dt.datetime.now().day).zfill(2)
        month = str(dt.datetime.now().month).zfill(2)
        date = f"{dt.datetime.now().year}-{month}-{day}"
        filename = str(last_post.roll + 1)
        file = request.files["Image"]
        title = request.form["Title"]
        content = request.files["Text"]

        if not allowed_file_txt(content.filename):
            raise BusinessValidationError(400, "POST001", "Invalid file type")

        content = request.files["Text"].read().decode('utf8')

        if not allowed_file_img(file.filename):
            raise BusinessValidationError(400, "POST001", "Invalid file type")

        post = Post(
            author=username,
            img=filename,
            text=content,
            date=date,
            title=title,
            views=0,
            likes=0
        )

        filepath = os.path.join(UPLOAD_FOLDER+"Posts/", filename +".webp")
        with open(filepath, 'wb') as f:
            f.write(convert_to_webp(file))

        db.session.add(post)
        db.session.commit()
        cache.clear()

        return post.to_dict()

comparse = reqparse.RequestParser()
comparse.add_argument("Comment")

class CommentAPI(Resource):
    def get(self, post_id):
        post = get_post_roll(post_id)
        if not post:
            raise NotFoundError(404, "Post not found")
        comments = get_comments_post(post_id)

        return [comment.to_dict() for comment in comments]

    def post(self, post_id):
        authorization_header = request.headers.get("Authorization", None)
        if not authorization_header:
            raise NotAuthorizedError(401, "No Token Provided")

        auth_token = authorization_header.split()[1]
        token = Token.query.filter_by(token=auth_token).first()

        if not token:
            raise NotAuthorizedError(401, "Invalid Token")

        user = User.query.filter_by(roll=token.user).first()
        username = user.username

        post = Post.query.filter_by(roll=post_id).first()
        if not post:
            raise NotFoundError(404, "Post not found")

        comment = comparse.parse_args().get("Comment", None)
        user = User.query.filter_by(username=username).first()

        if not user:
            raise BusinessValidationError(400, "COMMENT001", "Invalid Username")

        if not comment:
            raise BusinessValidationError(400, "COMMENT002", "No Comment Provided")

        new_comment = Comment(author=user.username, post=post_id, comment=comment)
        db.session.add(new_comment)
        db.session.commit()

        cache.delete_memoized(get_comments_post, post_id)

        return [new_comment.to_dict()]


class FollowerAPI(Resource):
    def get(self, username):
        user = get_user_username(username)
        if not user:
            raise NotFoundError(404, "User not found")
        following = get_followers(user.roll)

        return [follow.to_dict() for follow in following]

class FollowingAPI(Resource):
    def get(self, username):
        user = get_user_username(username)
        if not user:
            raise NotFoundError(404, "User not found")
        follows = get_follows(user.roll)

        return [follow.to_dict() for follow in follows]

    def post(self, username):
        authorization_header = request.headers.get("Authorization", None)
        if not authorization_header:
            raise NotAuthorizedError(401, "No Token Provided")

        auth_token = authorization_header.split()[1]
        token = Token.query.filter_by(token=auth_token).first()

        if not token:
            raise NotAuthorizedError(401, "Invalid Token")

        user = get_user_roll(token.user)
        if not user:
            raise BusinessValidationError(400, "COMMENT001", "Invalid Username")

        follow = get_user_username(username)
        if not follow:
            raise NotFoundError(404, "User not found")

        if Follow.query.filter_by(follower=user.roll, following=follow.roll).first():
            raise DuplicationError(409, "Follow already exists")

        token_response = requests.get("http://localhost:2345/api/token-jwt", headers={"Authorization": authorization_header})
        token = token_response.json()["jwt"]

        follow_response = requests.post(f'http://localhost:2345/vueapp/user/{follow.username}/follows', headers={"Authorization": token})

        return "Successfully Followed"

    def delete(self, username):
        authorization_header = request.headers.get("Authorization", None)
        if not authorization_header:
            raise NotAuthorizedError(401, "No Token Provided")

        auth_token = authorization_header.split()[1]
        token = Token.query.filter_by(token=auth_token).first()

        if not token:
            raise NotAuthorizedError(401, "Invalid Token")

        user = get_user_roll(token.user)
        if not user:
            raise BusinessValidationError(400, "COMMENT001", "Invalid Username")

        follow = get_user_username(username)
        if not follow:
            raise NotFoundError(404, "User not found")

        follow_record = Follow.query.filter_by(follower=user.roll, following=follow.roll).first()
        if not follow_record:
            raise NotFoundError(404, "Follow not found")

        token_response = requests.get("http://localhost:2345/api/token-jwt", headers={"Authorization": authorization_header})
        token = token_response.json()["jwt"]

        follow_response = requests.delete(f'http://localhost:2345/vueapp/user/{follow.username}/follows', headers={"Authorization": token})

        return "Successfully deleted"
