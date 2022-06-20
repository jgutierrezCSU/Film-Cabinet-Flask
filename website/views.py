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
    cur_pop_movies_lst = generate_curr_pop_movies()
    cur_pop_tv_show_lst = generate_curr_pop_tv_shows()

    # passes user to base, display certain items if logged in, else does not display
    return render_template(
        "home.html",
        user=current_user,
        cur_pop_movies_lst=cur_pop_movies_lst,
        cur_pop_tv_show_lst=cur_pop_tv_show_lst,
    )


def generate_curr_pop_movies():
    """https://developers.themoviedb.org/3/movies/get-popular-movies"""
    # from tmdb to get current popular movies , tmdb updates this API daily
    response = requests.get(
        "https://api.themoviedb.org/3/movie/popular?api_key="
        + config.api_key2
        + "&language=en-US&page=1"
    )

    cur_pop_movies_r = response.json()  # store parsed json response
    # list of dictionaries. each index is a dict
    fetched_cur_pop_movie_lst = cur_pop_movies_r["results"]
    # # get index position and display attributes
    # c = 0
    # for key, value in fetched_cur_pop_movie_lst[0].items():
    #     print(c, ":", key)
    #     c += 1

       
    # print(movie_provider_lst["rent"])
    # for i in movie_provider_lst["rent"]:
    #     print(i["provider_name"])
    # print(len(fetched_cur_pop_movie_lst))
    # Get data from retrieved lst dict and populate with relavent data
    cur_pop_movies_lst = []
    # cc=0
    for movie in fetched_cur_pop_movie_lst:
        cur_movie = {
            "id": movie["id"],
            "category": movie["genre_ids"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "overview": movie["overview"],
            "poster_path": movie["poster_path"],
            "default_image": "https://motivatevalmorgan.com/wp-content/uploads/2016/06/default-movie-1-1-300x450.jpg",
            "vote_average": movie["vote_average"],
            "image": f"https://image.tmdb.org/t/p/original/{movie['poster_path']}",
        }

        """ https://developers.themoviedb.org/3/movies/get-movie-details """
        # detaile for production status needed, checks if in theater(not streamable) or streamable
        # movie_details_request = requests.get(
        # "https://api.themoviedb.org/3/movie/"
        # + str(movie["id"])
        # + "?api_key="
        # + config.api_key2
        # +"&language=en-US"
        # )
        # cur_movie["status"].append(movie_details_request.json()["status"])
        # print("--------------\n",movie_details_request.json()["status"])
         
        movie_providers_request = requests.get(
        "https://api.themoviedb.org/3/movie/"
        + str(movie["id"])
        + "/watch/providers?api_key="
        + config.api_key2
        )
        # if cc==3 or cc ==2:
        #     movie_provider_lst = movie_providers_request.json()["results"]
        #     print(movie_provider_lst)
        # cc+=1
        movie_provider_lst = movie_providers_request.json()["results"]
        if movie_provider_lst:
            print(type(movie_provider_lst))
            # print(movie_provider_lst["US"]["rent"]["provider_name"])
            # cur_movie["provider_name"].append(movie_provider_lst["US"]["rent"]["provider_name"])
        else:
             cur_movie["provider_name"]="None Avaialable"
            
        # print("---------\n",movie_provider_lst['US'])
        # movie_provider_lst=movie_provider_lst["rent"]
        # print(movie_provider_lst)
        cur_pop_movies_lst.append(cur_movie)
        # print(cur_pop_movies_lst[0])

    return cur_pop_movies_lst


def generate_curr_pop_tv_shows():
    """https://developers.themoviedb.org/3/tv/get-popular-tv-shows"""
    # from tmdb to get current popular movies , tmdb updates this API daily
    response = requests.get(
        "https://api.themoviedb.org/3/tv/popular?api_key="
        + config.api_key2
        + "&language=en-US&page=1"
    )

    cur_pop_tv_shows_r = response.json()  # store parsed json response
    # list of dictionaries. each index is a dict
    fetched_cur_pop_tv_shows_lst = cur_pop_tv_shows_r["results"]
    # # get index position and display attributes
    # c = 0
    # for key, value in fetched_cur_pop_tv_shows_lst[0].items():
    #     print(c, ":", key)
    #     c += 1
    # print(fetched_cur_pop_tv_shows_lst[7])
    # Get data from retrieved lst dict and populate with relavent data
    cur_pop_tv_shows_lst = []
    for tv_show in fetched_cur_pop_tv_shows_lst:
        cur_movie = {
            "id": tv_show["id"],
            "category": tv_show["genre_ids"],
            "title": tv_show["name"],
            "release_date": tv_show["first_air_date"],
            "overview": tv_show["overview"],
            "poster_path": tv_show["poster_path"],
            "default_image": "https://motivatevalmorgan.com/wp-content/uploads/2016/06/default-tv_show-1-1-300x450.jpg",
            "vote_average": tv_show["vote_average"],
            "image": f"https://image.tmdb.org/t/p/original/{tv_show['poster_path']}",
        }
        cur_pop_tv_shows_lst.append(cur_movie)
        # print(cur_pop_movies_lst[0])

    return cur_pop_tv_shows_lst


def generate_random_movies():
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
    # end random Future
