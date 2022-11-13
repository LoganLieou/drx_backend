from flask import Flask, jsonify, request
import sqlite3
import numpy as np

app = Flask(__name__)

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
    like_city = [type(x) == int or type(x) == float for x in like_city]
    res = []
    for to_city in to_cities:
        # normalized cosine similarity * 100 = percent similarity
        # 1 = name
        # both are tuples
        name = to_city[1]
        to_city = [type(x) == int or type(x) == float for x in to_city]
        res.append([name, 1 / (1 + np.exp(-1*np.dot(like_city, to_city)))])
    return res

@app.route("/detail")
def detail():
    return jsonify()

@app.route("/send_city", methods=["POST"])
def send_preferences():
    if request.method == "POST":
        try:
            conn = sqlite3.connect("test.db")

            like = request.form['like']
            to = request.form['to']

            # DONE
            to_cities = conn.execute(f"""
                SELECT * FROM cities 
                WHERE seat = {to}
            """).fetchall()

            # TODO
            like_city = conn.execute(f"""
                SELECT * FROM cities 
                WHERE name = {like}
            """).fetchone()

            print(to_cities)
            print(like_city)

            res = similarity(to_cities, like_city)
            return jsonify(res)

        except Exception as e:
            return "ERROR: " + str(e)
    else:
        return "Try sending a post request instead..."

@app.route("/")
def index():
    return "api...def"
