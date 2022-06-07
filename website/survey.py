from flask import Blueprint, redirect, render_template, request
from flask_login import login_required, current_user
from .models import User
from . import db

# Blueprint allows you to define URL
survey = Blueprint("survey", __name__)


@survey.route("/survey", methods=["GET", "POST"])
def getSurveyInfo():
    if request.method == "POST":
        surveyData = request.form["data"]
        # print(surveyData)
        # user took survey so set to True
        usr_id = current_user.get_id()  # get UsersID
        # get user by that Unique ID
        user = User.query.filter_by(id=usr_id).first()
        user.took_survey = True
        db.session.commit()
    return render_template("survey.html", user=current_user)
