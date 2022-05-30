from flask import Blueprint, redirect, render_template,request,flash, url_for
from flask_login import  login_required, current_user
from .models import User

from . import db

#Blueprint allows you to define URL 
survey=Blueprint('survey',__name__)

@survey.route('/survey',methods=["GET","POST"])
def getSurveyInfo():
    if request.method == 'POST':
        surveyData = request.form['data']
        print(surveyData)
        #user took survey , set to true
        usrId=current_user.get_id()
        print("cur_userId:" ,usrId )
        user = User.query.filter_by(id=usrId).first()
        print("usr_db",user.took_survey)
        user.took_survey=True
        print("usr_db",user.took_survey)
        db.session.commit()

    return render_template("survey.html" ,user=current_user) 