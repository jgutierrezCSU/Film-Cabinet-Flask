from website import db
from website.models import User, Profile
from werkzeug.security import generate_password_hash, check_password_hash


def test_user():
    """
    Given a User model
    When new User is created
    Then checks that attributes are assigned correctly
    """
    user = User(
        id=1,
        email="test_email",
        password=generate_password_hash("password", method="sha256"),
        user_name="test_user_name",
        took_survey=True,
    )

    assert user.id == 1
    assert user.email == "test_email"
    # check password hash will return True or False
    assert check_password_hash(user.password, "password")
    assert user.user_name == "test_user_name"
    assert user.took_survey == True


def test_profile():
    """
    Given a Profile model
    When on creation and user updates profile
    Then checks that attributes are assigned correctly
    """
    profile = Profile(
        id=1,
        country="test_country",
        full_name="test_full_name",
        dob="01/01/01",
        user_id=1,
    )
    assert profile.id == 1
    assert profile.country == "test_country"
    assert profile.full_name == "test_full_name"
    assert profile.dob == "01/01/01"
    assert profile.user_id == 1
