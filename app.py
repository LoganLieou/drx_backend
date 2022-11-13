from flask import Flask, jsonify, request
import sqlite3
import numpy as np
import requests
import os
import json

app = Flask(__name__)

cache = {}

def similarity(to_cities, like_city):
    """
    return the list of to_cities in ranked order
    based on similarity

    columns:
    - cost_of_living
    - walkability
    - pubic_school_ranking
    - arts_and_culture_ranking
    - temprature
    - noise
    - crime rate
    - percepitation
    - air quality
    - housing price
    - age
    """
    like_city = like_city[2:]
    res = []
    for to_city in to_cities:
        # normalized cosine similarity * 100 = percent similarity
        # 1 = name
        # both are tuples
        name = to_city[1]
        to_city = to_city[2:]
        cosine_similarity = np.dot(like_city, to_city) / (np.linalg.norm(like_city) * np.linalg.norm(to_city))
        res.append([name, 1 / (1 + np.exp(-1*cosine_similarity))])
    return res

@app.route("/detail")
def detail():
    # return the cache front end can use it
    return jsonify(cache)

@app.route("/send_city", methods=["POST", "GET"])
def send_preferences():
    if request.method == "POST":
        try:
            # TODO replace with cockroach db connection
            # deploy cockroach db using cockroach cloud
            # just need actual connection string
            conn = sqlite3.connect("test.db")

            # information that is being sent from the frontend
            like = request.form['like']
            radius = request.form['radius']
            to = request.form['to']

            # getting the city we want it to be like from the database
            # to compare to
            like_city = conn.execute(f"""
                SELECT * FROM cities WHERE name = {like}
            """).fetchone()

            # get the zip code of the city we're moving to
            to_city_zip = conn.execute(f"""
                SELECT zip FROM cities WHERE name = {to}
            """).fetchone()

            # list of zipcodes using that one API
            url = f"""
                https://www.zipcodeapi.com/rest/{os.getenv("API_KEY")}/radius.json/{to_city_zip}/{radius}/mile
            """
            list_of_zipcodes = requests.get(url=url).json()

            # handle when zipcodes are empty
            # i.e. when we match no zipcodes
            if list_of_zipcodes == {}: 
                return "LOL no zipcodes match your location and/or radius preferences"

            # very scuffed way lots of sql queries going on here
            # this is O(n) queries instead of O(1) 😔
            to_cities = []
            for zipcode in list_of_zipcodes['zip_codes']:
                to_cities.append(conn.execute(f"""
                    SELECT * FROM cities WHERE zip = {zipcode['zip_code']}
                """).fetchone())
            to_cities = [x for x in to_cities if x]
            print(to_cities)

            # need the tuple index for the name of the city
            # cache this
            # TODO verify this works
            cache[like_city[1]] = to_cities

            # return similarity score json
            return jsonify(similarity(to_cities, like_city))

        except Exception as e:
            # catch exceptions
            return "ERROR: " + str(e)
    else:
        # tell the user to send post request instead
        # ig this is not possible since the endpoint won't receive get requests
        return "Try sending a post request instead..."

@app.route("/")
def index():
    return "api...def"
