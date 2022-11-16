from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import numpy as np
import requests
import os
import json

app = Flask(__name__)

CORS(app)

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
        # the cosine similarity is most accurate representation
        # of a ranked similarity score but the scores really don't mean
        # anything to a human need to find a way to normalize these properly
        # error due to very large values on some features i.e. home value
        name = to_city[1]
        zip_code = to_city[0]
        to_city = to_city[2:]
        score = np.dot(to_city, like_city) / (np.linalg.norm(to_city) * np.linalg.norm(like_city))

        # the reason we're returning zip code is because front end will
        # need to query to_zipcode like_zipcode for detail veiw if we want this feature
        # on frontend just like .name and .score need to be used unless we also want .zip_code
        res.append([zip_code, name, score])
    return res

@app.route("/detail", methods=["POST", "GET"])
def detail():
    if request.method == "POST":
        try:
            # these are zipcodes
            to = request.form['to_zipcode']
            like = request.form['like_zipcode']

            # return the cache front end can use it
            conn = sqlite3.connect("test.db")
            return jsonify((conn.execute(f"SELECT * FROM cities WHERE zip = {to}").fetchone(),
                            conn.execute(f"SELECT * FROM cities WHERE zip = {like}").fetchone()))
        except Exception as e:
            return "ERROR: " + str(e)
    else:
        return "try POST instead"

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
            # yes the key is public in our source code in plaintext lol
            # I mean bruh what u gonna do w this rate limit our site lmaooo bruh it's already limited to 10
            # calls / hr not gonna do shit my guy
            url = f"https://www.zipcodeapi.com/rest/xk98MBBMmDWguQK450Ev5dMTIrNa5Ioc5urBoxe2eONkWyyP49LAeY2DOUf3jZhW/radius.json/{to_city_zip[0]}/{radius}/mile"
            print(url)
            list_of_zipcodes = requests.get(url=url).json()

            # mocking bc rate limited :sadge:
            # with open("mock.json", "r") as f:
            #   list_of_zipcodes = json.loads(f.read())
            # print(list_of_zipcodes)

            # handle when zipcodes are empty
            # i.e. when we match no zipcodes
            if not list_of_zipcodes:
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
