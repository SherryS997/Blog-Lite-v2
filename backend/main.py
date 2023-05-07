import redis
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from application.database import db
from application.config import Config, KEY
from application import workers

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    with open(KEY) as key_file:
        app.secret_key = bytes(key_file.readline(), 'utf-8')
    app.app_context().push()

    # Initialize database
    db.init_app(app)
    app.app_context().push()

    # Initialize Celery
    celery = workers.celery
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.Task = workers.ContextTask
    app.app_context().push()

    return app, celery

app, celery = create_app()

# Initialize API
from application.api import UserAPI, PostAPI, CommentAPI, FollowerAPI, FollowingAPI
api = Api(app)
api.add_resource(UserAPI, "/api/user/<username>", "/api/user")
api.add_resource(PostAPI, "/api/post/id/<post_id>", "/api/post", "/api/post/user/<post_id>")
api.add_resource(CommentAPI, "/api/post/<int:post_id>/comment")
api.add_resource(FollowerAPI, "/api/user/<username>/followers")
api.add_resource(FollowingAPI, "/api/user/<username>/follows")

from application.routes import *

# Run application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2345)
