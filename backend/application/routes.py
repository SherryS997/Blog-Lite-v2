from flask import current_app as app
from flask import request, render_template
from application.models import db, User, Post, Comment, Follow, Token, Likes
from application.validation import BusinessValidationError, NotFoundError, NotAuthorizedError
from application.config import UPLOAD_FOLDER
from application.utils import convert_to_webp, create_analytics
from application.data_access import *
from application.tasks import importBlogs
from passlib.hash import pbkdf2_sha256 as passhash
import secrets, jwt, os, csv
import datetime as dt
from datetime import timedelta
from application.cache import cache

@app.route("/")
def home():
    return "Success", 200

@app.route("/vueapp/user/import", methods=["POST"])
def import_blogs():
    auth_header = request.headers.get("Authorization").split(" ")[1]
    if not auth_header:
        raise NotAuthorizedError(401, "No token provided.")
    token = jwt.decode(auth_header, app.secret_key, algorithms="HS256").get("token")
    token_id = Token.query.filter_by(token=token).first()
    if not token_id:
        raise NotAuthorizedError(401, "Invalid token.")
    user = get_user_roll(token_id.user)
    import_file = request.files["Import"]
    file_path = f"{user.username}.zip"
    with open(file_path, "wb") as file:
        file.write(import_file.stream.read())
    job = importBlogs.delay(file_path, user.username)
    try:
        return "Success"
    finally:
        while job.status != "SUCCESS":
            pass
        cache.clear()

@app.route("/97NBUmvRLiA4mz6Or6aadsflQj8Pt1slyRHnZitcsdMPOy8bHp3w6PcdIm2diYU/<username>")
def article_pdf(username):
    posts = get_posts_author(username)

    return render_template("article.html", posts = posts, username = username)

@app.route("/vueapp/user/export")
def blog_export():
    auth_header = request.headers.get("Authorization").split(" ")[1]
    if not auth_header:
        raise NotAuthorizedError(401, "No token provided.")
    token = jwt.decode(auth_header, app.secret_key, algorithms="HS256").get("token")
    token_id = Token.query.filter_by(token=token).first()
    if not token_id:
        raise NotAuthorizedError(401, "Invalid token.")
    user = get_user_roll(token_id.user)
    tasks.export.delay(user.username)
    return "200"

@app.route("/vueapp/analytics/export_data")
def export_data():
    auth_header = request.headers.get("Authorization").split(" ")[1]
    if not auth_header:
        raise NotAuthorizedError(401, "No token provided.")
    token = jwt.decode(auth_header, app.secret_key, algorithms="HS256").get("token")
    token_id = Token.query.filter_by(token=token).first()
    if not token_id:
        raise NotAuthorizedError(401, "Invalid token.")
    user = get_user_roll(token_id.user)
    tasks.export_csv.delay(user.username)
    return "200"

@app.route("/97NBUmvRLiA4mz6Or6ZWF24lQj8Pt1slyRHnZitcsdMPOy8bHp3w6PcdIm2diYU/<username>")
def report(username):
    user = get_user_username(username).to_dict()
    posts = get_posts_author_desc(username)
    has_posts = bool(posts)
    posts_data = [[post.title, post.views, post.likes, len(get_comments_post(post.roll))] for post in posts]

    if has_posts:
        create_analytics(username)

    data = {
        "user": user,
        "posts": posts_data,
    }
    return render_template("report.html", data=data, state=has_posts)

from application import tasks

@app.route("/vueapp/analytics")
def analytics():
    auth_header = request.headers.get("Authorization").split(" ")[1]
    if not auth_header:
        raise NotAuthorizedError(401, "No token provided.")
    token = jwt.decode(auth_header, app.secret_key, algorithms="HS256").get("token")
    token_id = Token.query.filter_by(token=token).first()
    if not token_id:
        raise NotAuthorizedError(401, "Invalid token.")
    user = get_user_roll(token_id.user)
    create_analytics(user.username)
    return "Successful"

@app.route("/vueapp/<string:username>/follows")
def FollowsUserVueAPI(username):
    users = get_follows(get_user_username(username).roll)
    out_users = []
    for following in users:
        user = get_user_roll(following.following)
        if user.username != "[deleted]":
            followers = len(get_followers(user.roll))
            follows = len(get_follows(user.roll))
            articles = len(get_posts_author(user.username))
            user = user.to_dict()
            user["follows"] = follows
            user["followers"] = followers
            user["articles"] = articles
            out_users.append(user)

    return out_users

@app.route("/vueapp/<string:username>/followers")
def FollowersUserVueAPI(username):
    out_users = []
    users = get_followers(get_user_username(username).roll)
    for follower in users:
        user = get_user_roll(follower.follower)
        if user.username != "[deleted]":
            followers = len(get_followers(user.roll))
            follows = len(get_follows(user.roll))
            articles = len(get_posts_author(user.username))
            user = user.to_dict()
            user["follows"] = follows
            user["followers"] = followers
            user["articles"] = articles
            out_users.append(user)

    return out_users

@app.route("/vueapp/search=<string:term>")
@cache.memoize()
def SearchVueAPIget(term):
    out_users = []
    users = User.query.filter(User.username.like(f"%{term}%")).all()
    posts = Post.query.filter(Post.title.like(f"%{term}%")).all()
    posts = [post.to_dict() for post in posts]
    for user in users:
        if user.username != "[deleted]":
            followers = len(get_followers(user.roll))
            follows = len(get_follows(user.roll))
            articles = len(get_posts_author(user.username))
            user = user.to_dict()
            user["follows"] = follows
            user["followers"] = followers
            user["articles"] = articles
            out_users.append(user)

    return { "users": out_users, "posts": posts }

@app.route("/vueapp/token")
def get_user_from_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise NotAuthorizedError(401, "No Token Provided")
    token = auth_header.split(" ")[1]
    decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
    token_obj = Token.query.filter_by(token=decoded_token.get("token")).first()
    if not token_obj:
        raise NotAuthorizedError(401, "Invalid Token")
    user = get_user_roll(token_obj.user)
    return user.to_dict()

@app.route("/vueapp/usertoken")
def TokenVueAPI():
    token = request.headers.get("Authorization", "").split(" ")[-1]
    try:
        decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        raise NotAuthorizedError(401, "Invalid token")

    token_value = decoded_token.get("token")
    if token_value is None:
        raise NotAuthorizedError(401, "No token provided")

    return {"token": token_value}

@app.route('/api/token-jwt')
def generate_jwt_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise NotAuthorizedError(401, "No token provided")

    token = auth_header.split()[1]
    encoded_token = jwt.encode({"token": token}, app.secret_key)

    return {"jwt": encoded_token}

@app.route("/vueapp/login", methods=["POST"])
def login_vue_post():
    data = request.get_json()
    username, password = data.get("username"), data.get("password")
    user = get_user_username(username)
    if not user:
        return {"error": 404, "error_msg": "User not found"}
    if not passhash.verify(password, user.password):
        return {"error": 401, "error_msg": "Invalid Password"}
    token = Token.query.filter_by(user=user.roll).first().token
    encoded_token = jwt.encode({"token": token}, app.secret_key)
    expiry_time = dt.datetime.utcnow() + timedelta(days=30)
    return {"token": encoded_token, "exp": expiry_time}

@app.route("/vueapp/user/<username>")
def user_vue_api_get(username):
    user = get_user_username(username)
    if user:
        return user.to_dict()
    else:
        raise NotFoundError(404, "User not found")

@app.route("/vueapp/user", methods=["POST", "PUT", "DELETE"])
def user_vue_api():
    if request.method == "PUT":
        auth = request.headers.get("Authorization", "").split(" ")[1]
        try:
            token = jwt.decode(auth, app.secret_key, algorithms="HS256").get("token")
        except:
            raise NotAuthorizedError(401, "Invalid Token")
        
        token_obj = Token.query.filter_by(token=token).first()
        if not token_obj:
            raise NotAuthorizedError(401, "Invalid Token")
        
        user = User.query.filter_by(roll=token_obj.user).first()
        if not user:
            raise NotFoundError(404, "User not found")

        if "New Username" in request.form and request.form["New Username"]:
            new_username = request.form["New Username"]
            posts = Post.query.filter_by(author=user.username).all()
            comments = Comment.query.filter_by(author=user.username).all()
            user.username = new_username
            for comment in comments:
                comment.author = new_username
            for post in posts:
                post.author = new_username

        if "New Password" in request.form and request.form["New Password"]:
            new_password = request.form["New Password"]
            if len(new_password) < 4:
                raise BusinessValidationError(400, "USER002", "Password should be at least 4 characters long")
            user.password = passhash.hash(new_password)

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
            filepath = os.path.join(UPLOAD_FOLDER + "Users/", user.img + ".webp")
            with open(filepath, 'wb') as f:
                f.write(convert_to_webp(file))

        cache.clear()
        db.session.commit()

        return "Successful"
    
    if request.method == "DELETE":
        auth_token = request.headers.get("Authorization", "").split(" ")[1]
        try:
            decoded_token = jwt.decode(auth_token, app.secret_key, algorithms=["HS256"])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            raise NotAuthorizedError(401, "Invalid or expired token")
        
        token = Token.query.filter_by(token=decoded_token.get("token")).first()
        if not token:
            raise NotAuthorizedError(401, "Invalid token")
        
        user = get_user_roll(token.user)
        if not user:
            raise NotFoundError(404, "User not found")
        
        posts = Post.query.filter_by(author=user.username).all()
        comments = Comment.query.filter_by(author=user.username).all()
        Token.query.filter_by(user=user.roll).delete()
        Follow.query.filter_by(follower=user.roll).delete()
        Follow.query.filter_by(following=user.roll).delete()

        for comment in comments:
            comment.author = "[deleted]"
        for post in posts:
            post.author = "[deleted]"

        if int(user.img) != 0:
            os.remove(UPLOAD_FOLDER + "Users/" + user.img + ".webp")

        Token.query.filter_by(user=user.roll).delete()
        User.query.filter_by(username=user.username).delete()

        cache.clear()
        db.session.commit()
        return "Successfully deleted"

    if request.method == "POST":
        json = request.get_json()
        username = json.get("Username")
        email = json.get("Email")
        password = json.get("Password")

        if not username:
            raise BusinessValidationError(400, "USER003", "Username is required")
        if not email:
            raise BusinessValidationError(400, "USER004", "Email is required")
        if not password or len(password) < 4:
            raise BusinessValidationError(400, "USER002", "Password should be at least 4 characters long")

        if get_user_username(username):
            return {"error": 409, "error_msg": "Username already exists"}
        if User.query.filter_by(email=email).first():
            return {"error": 409, "error_msg": "Email already exists"}

        user = User(
            username=username,
            email=email,
            password=passhash.hash(password),
            img=0,
            posted=0,
            pdf=0,
        )
        db.session.add(user)
        db.session.commit()

        token = Token(user=user.roll, token=secrets.token_urlsafe(32))
        db.session.add(token)
        db.session.commit()

        cache.clear()
        token = token.token
        encoded = jwt.encode({"token": token}, app.secret_key)
        expiry_time = dt.datetime.utcnow() + timedelta(days=30)
        return {"token": encoded, "exp": expiry_time}

@app.route("/vueapp/post/<string:token_id>")
def post_vue_api_get(token_id):
    if token_id == "all":
        contents = get_content_all()
        out = [{"post": post.to_dict(), "user": user.to_dict()} for post, user in contents]
        return out

    user = get_user_username(token_id)
    if user:
        posts = get_posts_author_desc(user.username)
        out = [post.to_dict() for post in posts]
        return out

    decoded_token = jwt.decode(token_id, app.secret_key, algorithms="HS256").get("token")
    token = Token.query.filter_by(token=decoded_token).first()
    if token:
        user = get_user_roll(token.user)
        follows = [get_user_roll(f.following).username for f in get_follows(user.roll)]
        contents = get_content_user(follows)
        out = [{"post": post.to_dict(), "user": user.to_dict()} for post, user in contents]
        return out

@app.route("/vueapp/post/<int:post_id>", methods=["GET", "PUT", "DELETE"])
def post_vue_api(post_id):
    if request.method == "GET":
        post = get_post_roll(post_id)
        if post:
            post.views += 1
            db.session.commit()
            author = get_user_username(post.author).to_dict()
            out = {"post": post.to_dict(), "author": author}
            return out
        else:
            raise NotFoundError(404, "Post not found")

    if request.method == "PUT":
        auth = request.headers.get("Authorization", "").split(" ")[1]
        try:
            decoded_token = jwt.decode(auth, app.secret_key, algorithms="HS256").get("token")
            token = Token.query.filter_by(token=decoded_token).first()
            if not token:
                raise NotAuthorizedError(401, "Invalid Token")
            user = get_user_roll(token.user)
            if not user:
                raise NotFoundError(404, "User not found")
            post = Post.query.get(post_id)
            if not post:
                raise NotFoundError(404, "Post not found")
            if request.files:
                file = request.files['file']
                filename = file.filename
                filepath = os.path.join(UPLOAD_FOLDER, "Posts", post.img + ".webp")
                with open(filepath, 'wb') as f:
                    f.write(convert_to_webp(file))
            post.title = request.form["title"]
            post.text = request.form["content"]
            cache.clear()
            db.session.commit()
            return "Successfully updated"
        except (IndexError, ValueError, KeyError):
            raise NotAuthorizedError(401, "No Token Provided")
    
    if request.method == "DELETE":
        auth_token = request.headers.get("Authorization", "").split(" ")[1]
        decoded_token = jwt.decode(auth_token, app.secret_key, algorithms="HS256").get("token")
        token = Token.query.filter_by(token=decoded_token).first()
        if not decoded_token:
            raise NotAuthorizedError(401, "No valid token provided")
        user = get_user_roll(token.user)
        if not user:
            raise NotFoundError(404, "User not found")
        post = get_post_roll(post_id)
        if not post:
            raise NotFoundError(404, "Post not found")
        if post.author != user.username:
            raise NotAuthorizedError(401, "Invalid token")
        Comment.query.filter_by(post=post_id).delete()
        os.remove(os.path.join(UPLOAD_FOLDER, "Posts", f"{post.img}.webp"))
        db.session.delete(post)
        cache.clear()
        db.session.commit()
        return "Successfully deleted"

@app.route("/vueapp/post", methods=["POST"])
def post_vue_api_post():
    auth = request.headers.get("Authorization")
    if not auth:
        raise NotAuthorizedError(401, "No Token Provided")
    token = auth.split(" ")[1]
    try:
        decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"]).get("token")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise NotAuthorizedError(401, "Invalid Token")
    token = Token.query.filter_by(token=decoded_token).first()
    user = get_user_roll(token.user)
    if not user:
        raise NotFoundError(404, "User not found")
    last_post = Post.query.order_by(Post.roll.desc()).first()
    now = dt.datetime.now()
    filename = str(last_post.roll + 1)
    file = request.files["file"]
    title = request.form["title"]
    content = request.form["content"]
    if not allowed_file_img(file.filename):
        raise BusinessValidationError(400, "POST001", "Invalid file type")
    post = Post(
        author=user.username,
        img=filename,
        text=content,
        date=now.strftime("%Y-%m-%d"),
        title=title,
        views=0,
        likes=0,
    )
    filepath = os.path.join(UPLOAD_FOLDER, "Posts", f"{filename}.webp")
    with open(filepath, "wb") as f:
        f.write(convert_to_webp(file))
    cache.clear()
    user.posted = 1
    db.session.add(post)
    db.session.commit()
    return "Successfully posted"


@app.route("/vueapp/post/<int:post_id>/comment", methods=["POST", "GET"])
def CommentVueAPI(post_id):
    if request.method == "GET":
        post = get_post_roll(post_id)
        if not post:
            raise NotFoundError(404, "Post not found")
        comments = get_comments_post(post_id)
        return [comment.to_dict() for comment in comments]

    if request.method == "POST":
        auth = request.headers.get("Authorization")
        if not auth:
            raise NotAuthorizedError(401, "No Token Provided")
        token = auth.split(" ")[1]
        decoded_token = jwt.decode(token, app.secret_key, algorithms="HS256").get("token")
        token = Token.query.filter_by(token=decoded_token).first()
        if not token:
            raise NotAuthorizedError(401, "Invalid Token")
        user = get_user_roll(token.user)
        post = get_post_roll(post_id)
        if not post:
            raise NotFoundError(404, "Post not found")
        comment_text = request.get_json().get("Comment")
        comment = Comment(author=user.username, post=post_id, comment=comment_text)
        cache.delete_memoized(get_comments_post, post_id)
        db.session.add(comment)
        db.session.commit()
        return "Successfully commented"

@app.route("/vueapp/user/<username>/followers")
def FollowerVueAPI(username):
    user = get_user_username(username)
    if not user:
        raise NotFoundError(404, "User not found")
    following = get_followers(user.roll)

    return [follow.to_dict() for follow in following]

@app.route("/vueapp/user/<username>/follows", methods=["GET", "POST", "DELETE"])
def following_vue_api(username):
    user = get_user_username(username)
    if not user:
        raise NotFoundError(404, "User not found")

    if request.method == "GET":
        follows = get_follows(user.roll)
        return [follow.to_dict() for follow in follows]

    if "Authorization" not in request.headers:
        raise NotAuthorizedError(401, "No Token Provided")
    auth = request.headers["Authorization"].split(" ")[1]
    auth = jwt.decode(auth, app.secret_key, algorithms="HS256").get("token")
    user_token = Token.query.filter_by(token=auth).first()
    if not user_token:
        raise NotAuthorizedError(401, "Invalid Token")
    current_user = get_user_roll(user_token.user)
    if not current_user:
        raise BusinessValidationError(400, "COMMENT001", "Invalid Username")

    follow = get_user_username(username)
    if not follow:
        raise BusinessValidationError(400, "COMMENT001", "Invalid Username")

    if request.method == "POST":
        state = Follow.query.filter_by(follower=current_user.roll, following=follow.roll).first()
        if not state:
            follow = Follow(follower=current_user.roll, following=follow.roll)
            db.session.add(follow)
            db.session.commit()
            cache.clear()
        return "Successfully posted"

    if request.method == "DELETE":
        state = Follow.query.filter_by(follower=current_user.roll, following=follow.roll).first()
        if state:
            Follow.query.filter_by(follower=current_user.roll, following=follow.roll).delete()
            db.session.commit()
            cache.clear()
        return "Successfully deleted"

@app.route("/vueapp/likes/<string:user>/<int:post>")
def LikesVueAPIget(user, post):
    user = get_user_username(user).roll
    like = get_like_status(user, post)
    
    return {"status":"true" if like else "false"}

@app.route("/vueapp/like/<int:post_id>", methods=["POST", "DELETE"])
def likes_vue_api(post_id):
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise NotAuthorizedError(401, "No Token Provided")
    auth_token = auth_token.split(" ")[1]
    decoded_token = jwt.decode(auth_token, app.secret_key, algorithms="HS256").get("token")
    token = Token.query.filter_by(token=decoded_token).first()
    user = get_user_roll(token.user)
    post = Post.query.filter_by(roll=post_id).first()
    if not post:
        raise NotFoundError(404, "Post not found")
    
    if request.method == "POST":
        post.likes += 1
        like = Likes(user=user.roll, post=post.roll)
        db.session.add(like)
        cache.clear()
        db.session.commit()

        return "Successfully posted"

    elif request.method == "DELETE":
        post.likes -= 1
        Likes.query.filter_by(user=user.roll, post=post.roll).delete()
        cache.clear()
        db.session.commit()

        return "Successfully deleted"


@app.route("/vueapp/<follower>/follows/<following>")
def check_follow(follower, following):
    follower_obj = get_user_username(follower)
    following_obj = get_user_username(following)

    if not (follower_obj and following_obj):
        return "Failed", 404

    status = get_follow_status(follower_obj.roll, following_obj.roll)
    return status
