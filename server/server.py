from flask import Flask, make_response, send_from_directory, send_file, abort, jsonify, request, json
from flask_cors import CORS, cross_origin
import pandas as pd

from models.knn import getNeighbors

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


"""
    START OF THE BASIC ROUTES
    =========================
"""
@app.route("/datasets/<csv_id>")
@cross_origin()
def get_csv(csv_id):

    filename = "./datasets/dataset.csv"
    dataset = pd.read_csv(filename, dtype=str)

    if csv_id == "movies":
        dataset = dataset[["movieId","title", "genres"]]

    try:
        return json.dumps({
            "ratings": dataset.to_dict(orient="records")
        })
    except FileNotFoundError:
        abort(404)


@app.route("/api/users/")
@cross_origin()
def get_users():
    filename = "./datasets/ratings.csv"
    dataset = pd.read_csv(filename, dtype=str)

    try:
        return json.dumps(list(dataset["userId"].unique()))
    except FileNotFoundError:
        abort(404)


@app.route("/api/movies/")
@cross_origin()
def get_movies():
    filename = "./datasets/dataset.csv"
    dataset = pd.read_csv(filename, dtype=str)
    dataset = dataset[["movieId", "title", "genres"]]

    try:
        return json.dumps(dataset.to_dict(orient="records"))
    except FileNotFoundError:
        abort(404)


"""
    END OF THE BASIC ROUTES
    ========================
"""

#-----------------------------------------------------------------------------------------------

"""
    START OF THE LOGICAL ROUTES
    ===========================
"""

@app.route("/api/algorithm/collab/movie/<movie_id>/<k_neighboors>")
@cross_origin()
def find_similar_knn(movie_id, k_neighboors):
    filename = "./datasets/dataset.csv"
    movies = pd.read_csv(filename, dtype=str)

    result = getNeighbors(movies, int(movie_id), int(k_neighboors))

    parsed_result = []
    for i in range(len(result)):
        parsed_result.append({"movieId": result[i]["movieId"].values[0], "title": result[i]["title"].values[0], "genres": result[i]["genres"].values[0]})

    try:
        return json.dumps(parsed_result)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
   app.run(debug=True)