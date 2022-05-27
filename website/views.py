from flask import Blueprint ,render_template

from website.auth import login
from flask_login import  login_required, current_user
#Blueprint allows you to define URL 

views=Blueprint('views',__name__)


@views.route('/')
@login_required
def home():
    #passes user to base, display certain items if logged in, else does not display 
    return render_template("home.html" , user=current_user) 

#defining views Blueprint
@views.route('/survey')
@login_required
def survey():
    #passes user to base, display certain items if logged in, else does not display 
    return render_template("survey.html" , user=current_user) 