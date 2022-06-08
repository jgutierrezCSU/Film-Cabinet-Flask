from flask import Flask, session
from sqlalchemy import func
from website import db
from website.models import User, Profile
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


# Initiate Database
def init_database():
    app = Flask(__name__)
    DB_NAME = "test_database.db"
    app.secret_key = "super secret keys" 
    app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = f"sqlite:///{DB_NAME}"  # store DB in directory
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app_contex=app.app_context()
    app_contex.push()
    db.create_all(app=app)
    return db, app_contex

def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

def test_user():
    """
    Given a User model
    When new User is created and inserted in Database
    Then checks that attributes/unique id are assigned correctly.
    """
    db , app_contex =init_database()
    count = User.query.count()
    count += 1
    user = User(
        email="test_email" + str(count) ,
        password=generate_password_hash("password", method="sha256"),
        user_name="test_user_name",
        took_survey=True,
    )

    #commit to Database
    db.session.add(user)
    db.session.commit()

    #acces from database
    assert user.id == count
    assert user.email == "test_email" + str(count)
    # check password hash will return True or False
    assert check_password_hash(user.password, "password")
    assert user.user_name == "test_user_name"
    assert user.took_survey == True

    # Tear Down Database
    # db.session.remove()
    # db.drop_all()
    # app_contex.pop()

    


def test_profile():
    """
    Given a Profile model
    When on creation and user updates profile
    Then checks that attributes/unique id are assigned correctly
    """
    db , app_contex =init_database()

    count = Profile.query.count()
    count+=1
    # Get just inserted users ID
    #user = User.query.first()

    profile = Profile(
        country="test_country",
        full_name="test_full_name",
        dob="01/01/01",
        user_id=count,
    )
    #commit to Database
    db.session.add(profile)
    db.session.commit()
    
    #acces from database
    assert profile.id == count
    assert profile.country == "test_country"
    assert profile.full_name == "test_full_name"
    assert profile.dob == "01/01/01"
    assert profile.user_id == count

    # Tear Down Database
    # db.session.remove()
    # db.drop_all()
    # app_contex.pop()

