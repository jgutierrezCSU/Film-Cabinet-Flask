from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()  # initialize DB Object
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.secret_key = "super secret keys"  # needed for creation of sessions
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"sqlite:///{DB_NAME}"  # store DB in directory
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .survey import survey
    from .user_profile import user_profile

    app.register_blueprint(views, url_prefix="/")  # no prefix
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(survey, url_prefix="/")
    app.register_blueprint(user_profile, url_prefix="/")

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # where to redirect if @login_required
    login_manager.init_app(app)

    # use this fucntion to load users
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # by default , looks for primary key

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
