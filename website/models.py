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
    first_name = db.Column(db.String(150))
    took_survey=db.Column(db.Boolean, default=func.now())
    notes = db.relationship('Note')