from flask import Blueprint ,render_template
from website.auth import login
from flask_login import  login_required, current_user
from .models import User 
from . import db 


#Blueprint allows you to define URL 
user_Profile=Blueprint('user',__name__)

@user_Profile.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(first_name=username).first_or_404()
    # print("N",user.first_name)
    # print("S",user.took_survey)
    posts = [
    	#pass user object to user.html
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)