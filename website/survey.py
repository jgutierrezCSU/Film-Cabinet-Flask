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
        print("here")
        return render_template("home.html",user=current_user ) 
    print("outside")
    return render_template("survey.html" ,user=current_user) 