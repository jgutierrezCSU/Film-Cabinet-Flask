from flask import Blueprint ,render_template,request,flash
from website.auth import login
from flask_login import  login_required, current_user
from .models import User, Profile
from . import db 


#Blueprint allows you to define URL 
user_profile=Blueprint('user_profile',__name__)

@user_profile.route('/user/<username>',methods=["GET","POST"])
@login_required
def user(username):
    curr_usr_id=current_user.get_id() #get curr user id
    #get user w/ that Unique ID
    user = User.query.filter_by(id=curr_usr_id).first() 
    #get profile w/ that Unique ID
    profile = Profile.query.filter_by(user_id=user.id).first()
    #gets form info after edited and saved
    if request.method == 'POST':
        new_fullname=request.form.get('edit_fullname')
        if new_fullname == "":
            new_fullname="Full Name"
        new_country=request.form.get('edit_country')
        if new_country == "":
            new_country="Country"
        new_dob=request.form.get('edit_dob')
        if new_dob == "":
            new_dob="MM/DD/YYYY"      
        else:
            user.full_name=new_fullname
            #user.email=new_email
            profile.country=new_country
            profile.full_name=new_fullname
            profile.dob=new_dob
            db.session.commit()
        
    #get user to send to front end
    user = User.query.filter_by(user_name=username).first_or_404()
    return render_template('user.html', user=user,profile=profile)
