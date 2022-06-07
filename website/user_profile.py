from flask import Blueprint, render_template, request, flash
from website.auth import login
from flask_login import login_required, current_user
from .models import User, Profile
from . import db


# Blueprint allows you to define URL
user_profile = Blueprint("user_profile", __name__)


@user_profile.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    curr_usr_id = current_user.get_id()  # get curr user id
    # get user w/ that Unique ID
    user = User.query.filter_by(id=curr_usr_id).first()
    # get profile w/ that Unique ID
    profile = Profile.query.filter_by(user_id=user.id).first()
    # gets form info after edited and saved
    if request.method == "POST":
        new_fullname = request.form.get("edit_fullname")
        if new_fullname == "":
            new_fullname = profile.full_name
        new_country = request.form.get("edit_country")
        if new_country == "":
            new_country = profile.country
        new_dob = request.form.get("edit_dob")
        if new_dob == "":
            new_dob = profile.dob
            print("1", new_fullname)
            print("1", new_country)
            print("1", new_dob)

        print(new_fullname)
        print(new_country)
        print(new_dob)
        profile.full_name = new_fullname
        profile.country = new_country
        profile.dob = new_dob
        db.session.commit()
        print("here")
    # get user to send to front end
    user = User.query.filter_by(user_name=username).first_or_404()
    return render_template("user.html", user=user, profile=profile)
