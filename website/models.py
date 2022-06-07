from email.policy import default
from . import db 
from flask_login import UserMixin 
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True) #Unique ID
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # One to many relationship , one user has many notes


class User(db.Model, UserMixin): #userMixin allows "current_user" module to acces current user
    id = db.Column(db.Integer, primary_key=True)#Unique ID
    email = db.Column(db.String(150), unique=True) #unique, no tother use can have same email
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    took_survey = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note')

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # profile_photo = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    #phonenumber = db.Column(db.Integer, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    #cascade = when user deleted: delete profile
    user = db.relationship('User', backref=db.backref('profile', cascade="all, delete-orphan"), lazy='joined')