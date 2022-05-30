from flask import Blueprint ,render_template

from website.auth import login
from flask_login import  login_required, current_user

from .models import User #testing for DB
from . import db #testing for DB


#Blueprint allows you to define URL 

views=Blueprint('views',__name__)


@views.route('/')
@login_required
def home():
	#for testing
	# usrId=current_user.get_id()
	# print("Home cur_userId:",usrId )
	# user = User.query.filter_by(id=usrId).first()
	# print("home usr_db",user.took_survey)
	#end testing

	#passes user to base, display certain items if logged in, else does not display 
	return render_template("home.html" , user=current_user) 

@views.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(first_name=username).first_or_404()
    print(user.first_name)
    posts = [
    	#pass user object to user.html
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)