import json
from flask import Blueprint, render_template
from os.path import exists
from website.auth import login
from flask_login import login_required, current_user

from .models import User
from . import db

import csv
import random
import requests
import config


# Blueprint allows you to define URL
views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    # for random Future
    # checks if server path exist
    server_path = exists("/var/www/Film-Cabinet-Flask/website/netflix_titles.csv")

    if server_path:
        data = list(
            csv.reader(
                open(
                    "/var/www/Film-Cabinet-Flask/website/netflix_titles.csv",
                    encoding="utf-8",
                )
            )
        )  # get CSV and turn into list
        # for loop to gey USA films
        while True:
            row = random.choice(data)  # get random row from csv
            if row[5] == "United States":
                break
    elif exists("website/netflix_titles.csv"):
        data = list(
            csv.reader(open("website/netflix_titles.csv", encoding="utf-8"))
        )  # get CSV and turn into list
        # for loop to gey USA films
        while True:
            row = random.choice(data)  # get random row from csv
            if row[5] == "United States":
                break

    # from tmdb
    response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=' +  config.api_key2 + '&primary_release_year=2020&sort_by=revenue.desc')
    highest_revenue = response.json() # store parsed json response
    highest_revenue_films = highest_revenue['results']
    # # get index position
    # c=0
    # for key, value in highest_revenue_films[0].items():
    #     print(c,":",key)
    #     c+=1
    # print(highest_revenue_films[-1])
    random_choice= random.randint(0,len(highest_revenue_films))
    # print(len(highest_revenue_films))
    # print(random_choice)

    movie = {
        "id": highest_revenue_films[random_choice]["id"],
        "category": highest_revenue_films[random_choice]["genre_ids"],
        "title": highest_revenue_films[random_choice]["title"],
        # "director": row[3],
        # "cast": row[4],
        # "country": row[5],
        "release_date": highest_revenue_films[random_choice]["release_date"],
        # "release_year": row[7],
        # "maturity": row[8],
        # "duration": row[9],
        # "genre": row[10],
        "overview":highest_revenue_films[random_choice]["overview"],
        "poster_path": highest_revenue_films[random_choice]['poster_path'],
        "default_image": "https://motivatevalmorgan.com/wp-content/uploads/2016/06/default-movie-1-1-300x450.jpg",
        "vote_average": highest_revenue_films[random_choice]["vote_average"],
        "image": f"https://image.tmdb.org/t/p/original/{highest_revenue_films[random_choice]['poster_path']}"
    }
    # url="https://api.themoviedb.org/3/movie/524047/watch/providers?api_key=a594b9969faa07c895f9e33649889404"
    # r=requests.request("GET",url)
    # print(r.json()['results'])
    # image="https://image.tmdb.org/t/p/original/wigZBAmNrIhxp2FNGOROUAeHvdh.jpg"
    # url = f"https://image.tmdb.org/t/p/original/{movie['poster_path']}"
    # get back the response
    # response = requests.request("GET", url)
    # parse result into JSON and look for matching data if available
    # movie_data = response.json()
    # print(movie_data)
    # if "Poster" in movie_data:
    #     movie["image"] = image
    # if "imdbRating" in movie_data:
    #     movie["imdb"] = movie_data["imdbRating"]

    # end random Future
    # passes user to base, display certain items if logged in, else does not display
    return render_template("home.html", user=current_user, movie=movie)
