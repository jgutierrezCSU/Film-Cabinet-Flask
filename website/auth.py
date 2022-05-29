from flask import Blueprint, redirect, render_template,request,flash, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from flask_login import login_user, login_required, logout_user, current_user

#Blueprint allows you to define URL 

auth=Blueprint('auth',__name__)

@auth.route('/login/',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        print("login POST")
        email = request.form.get('emailLogin')
        password = request.form.get('password')
        #find User w/ Email
        user = User.query.filter_by(email=email).first() # should only be one user w/ unique email
        if user: #if valid User Email
            print("valid user")
            #if correct PW
            if check_password_hash(user.password, password): #method for comparing hashed PW, and passed in Pw
                flash('Logged in successfully!', category='success')
                #log in user to a session
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            # Not correct PW
            else:
                print("pw No good")
                flash('Incorrect password, try again.', category='error')
        else: #not Valid User Email
                print("No email found")
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
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(email,first_name,password1,password2)

        #find User w/ Email
        #check if already a userw/ that email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Not Valid Email',category='error')
        elif len(first_name) < 2:
                flash('Enter Valid Name', category='error')
        elif password1 != password2:
                flash('Passwords Do Not Match.', category='error')
        elif len(password1) < 0:
                flash('Password must be at least 8 characters.', category='error')
        else:
            #store new user in DB
            #generate a hashed PW and store
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user) #add new user to DB
            db.session.commit() # update
            #log in user to a session
            login_user(new_user,remember=True)
            flash('Account created!', category='success')

            #redirect to survey page:
            return redirect(url_for('survey.getSurveyInfo'))
    return render_template("signup.html",user=current_user) # current_user from built in library