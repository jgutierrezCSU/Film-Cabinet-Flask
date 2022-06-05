from flask import Blueprint ,render_template
from os.path import exists
from website.auth import login
from flask_login import  login_required, current_user

from .models import User 
from . import db 

import csv
import random
import requests
import config


#Blueprint allows you to define URL 
views=Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    #for random Future
 
    # checks if local path exist
    local_path=exists('website/netflix_titles.csv')
    # checks if server path exist
    server_path=exists('/var/www/Film-Cabinet-Flask/website/netflix_titles.csv')

    if server_path:
        data = list(csv.reader(open('/var/www/Film-Cabinet-Flask/website/netflix_titles.csv',encoding='utf-8'))) # get CSV and turn into list
        #for loop to gey USA films
        while True:
            row = random.choice(data)# get random row from csv
            if row[5] == "United States":
                break
    elif local_path:
        data = list(csv.reader(open('website/netflix_titles.csv',encoding='utf-8'))) # get CSV and turn into list
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

