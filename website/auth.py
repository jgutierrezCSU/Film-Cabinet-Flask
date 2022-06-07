from flask import Blueprint, redirect, render_template,request,flash, url_for
from .models import User , Profile
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from flask_login import login_user, login_required, logout_user, current_user

#Blueprint allows you to define URL 

auth=Blueprint('auth',__name__)

@auth.route('/login/',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('emailLogin')
        password = request.form.get('password')
        #find User w/ Email
        user = User.query.filter_by(email=email).first() # should only be one user w/ unique email
        if user: #if valid User Email
            #if correct PW
            if check_password_hash(user.password, password): #method for comparing hashed PW, and passed in Pw
                flash('Logged in successfully!', category='success')
                #log in user to a session
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            # Not correct PW
            else:
                flash('Incorrect password, try again.', category='error')
        else: #not Valid User Email
                flash('Email does not exist, try again.', category='error')
    return render_template("login.html",user=current_user)

@auth.route('/logout/')
@login_required # can only acces if logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up/',methods=["GET","POST"])
def signup():

    if request.method == 'POST':
        #get Info from login.htnl after submit
        email = request.form.get('email')
        user_name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
       

        #find User w/ Email
        #check if already a userw/ that email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Not Valid Email',category='error')
        elif len(user_name) < 2:
                flash('Enter Valid Name', category='error')
        elif password1 != password2:
                flash('Passwords Do Not Match.', category='error')
        elif len(password1) < 0:
                flash('Password must be at least 8 characters.', category='error')
        else:
            #store new user in DB
            #generate a hashed PW and store
            new_user = User(email=email, user_name=user_name, password=generate_password_hash(
                password1, method='sha256'))

            db.session.add(new_user) #add new user to DB
            db.session.commit() # update
             #log in user to a session
            login_user(new_user,remember=True)

            #get new_user unique ID
            curr_usr_id=current_user.get_id() #get curr user id
            #also generate Profile DB w/ defaults
            user_profile = Profile(
                           country="Country",
                           full_name="Full Name",
                           dob="MM/DD/YYYY",
                           user_id=curr_usr_id
                           )
            db.session.add(user_profile)
            db.session.commit()
            flash('Account created!', category='success')
            #redirect to survey page:
            return redirect(url_for('survey.getSurveyInfo'))
    return render_template("signup.html",user=current_user) # current_user from built in library

@login_required
@auth.route('/update-cred/',methods=["GET","POST"])
def update_cred():
    #get curr user id
    curr_usr_id=current_user.get_id() 
    #get user object w/ that Unique ID
    user = User.query.filter_by(id=curr_usr_id).first() 
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_email = request.form.get('new_email') 

        #both empty , no need to write to DB
        if new_username == "" and new_email == "":
            return redirect(url_for('user_profile.user',username=current_user.user_name))

        # if either empty,Set to original creds
        if new_username == "":
            new_username = user.user_name
        if new_email == "":
            new_email =user.email

        if len(new_email) < 4:
            print('Not Valid Email')
        elif len(new_username) <= 0:
            print('Not Valid Username length')
        #find a user in DB w/ that email from input (Object)
        user_by_email = User.query.filter_by(email=new_email).first()
        found_email=False
        if user_by_email:
            found_email=user_by_email.email
            # TODO add flash error
        if found_email == new_email and user.email != new_email: 
            print('Email already exists.')
        else:
            #find a user in DB w/ that user_name from input (Object)
            user_by_uname = User.query.filter_by(user_name=new_username).first()
            found_uname=False
            if user_by_uname:
                found_uname=user_by_uname.user_name
                # TODO add flash error
            if found_uname == new_username and user.user_name != new_username: 
                print('User already exists.')
            else:
                user.user_name=new_username
                user.email=new_email
                db.session.commit()
                return redirect(url_for('user_profile.user',username=current_user.user_name))


    return render_template("update_cred.html",user=current_user) 

@login_required
@auth.route('/update-pword/',methods=["GET","POST"])
def update_pword():
    curr_usr_id=current_user.get_id() 
    #get user w/ that Unique ID
    user = User.query.filter_by(id=curr_usr_id).first() 
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        new_password2 = request.form.get('new_password2')

        # Input checks
        if new_password != new_password2:
            print('Passwords Do Not Match.')
        elif len(new_password) <= 0:
            print("Password must be at least 8 characters.")
        else:
            if new_password != "":
                user.password=generate_password_hash(new_password, method='sha256')
                db.session.commit()
            return redirect(url_for('user_profile.user',username=current_user.user_name))


    return render_template("update_pword.html",user=current_user) 