from flask import Blueprint ,render_template
from os.path import exists
from website.auth import login
from flask_login import  login_required, current_user

from .models import User #testing for DB
from . import db #testing for DB

import csv
import random
import requests
import config


#Blueprint allows you to define URL 
views=Blueprint('views',__name__)
def getUSMovie():
    pass


@views.route('/')
@login_required
def home():
    print("home")
    #for random Future
    #looks for file using server path
    try:
        # checks if local path exist
        local_path=exists('website/netflix_titles.csv')
        
    except:
        print("Local path not found: Trying server path")
    #looks for file in normal Python library
    try:
        # checks if server path exist
        server_path=exists('/var/www/Film-Cabinet-Flask/website/netflix_titles.csv')

    except:
        print("server path not found. Local path used")

    if local_path:
        data = list(csv.reader(open('website/netflix_titles.csv'))) # get CSV and turn into list
        #for loop to gey USA films
        while True:
            row = random.choice(data)# get random row from csv
            if row[5] == "United States":
                break
    else:
        data = list(csv.reader(open('website/netflix_titles.csv'))) # get CSV and turn into list
        #for loop to gey USA films
        while True:
            row = random.choice(data)# get random row from csv
            if row[5] == "United States":
                break

    movie = {
        'id': row[0],
        'category': row[1],
        'title': row[2],
        'director': row[3],
        'cast': row[4],
        'country': row[5],
        'date_added': row[6],
        'release_year': row[7],
        'maturity': row[8],
        'duration': row[9],
        'genre': row[10],
        'description': row[11],
        'image': 'https://motivatevalmorgan.com/wp-content/uploads/2016/06/default-movie-1-1-300x450.jpg',
        'imdb': 'Not Available'
        }

    # get cover image
    # call OMDB database
    url = f"http://www.omdbapi.com/?t={movie['title']}/&apikey={config.api_key}"
    # get back the response
    response = requests.request("GET", url)
    # parse result into JSON and look for matching data if available
    movie_data = response.json()
    if 'Poster' in movie_data:
        movie['image'] = movie_data['Poster']
    if 'imdbRating' in movie_data:
        movie['imdb'] = movie_data['imdbRating']

    #end random Future
    #passes user to base, display certain items if logged in, else does not display 
    return render_template("home.html" , user=current_user, movie=movie) 

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