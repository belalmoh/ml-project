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

#####################################################################33
# YOmna 

from sklearn.metrics.pairwise import cosine_similarity
def getNeighbors_KMeans(data, movieId, K):
    
    columns=['director_name', 'actor_2_name', 'actor_1_name', 
             'clean_title', 'actor_3_name', 'language', 'country','content_rating', 
             'genres', 'year', 'movieId', 'original_title', 'title', 'clusterLabel']
    
    # Centroids of trained clusters
    centroids = np.array([[9.36527906e+03, 6.41109944e+00, 2.88947752e+07, 7.96827436e+00,
        4.46312346e+07, 1.23634454e+00, 4.72864146e+00, 2.08928571e+00,
        3.15301120e+00, 3.37815126e+00, 8.62990196e+00, 4.79061625e+00,
        3.07142857e+00, 1.40056022e-03, 2.46848739e-01, 1.61414566e-01,
        3.36134454e-02, 6.47759104e-02, 5.60224090e-02, 4.34523810e-01,
        2.24789916e-01, 2.48599440e-02, 5.92787115e-01, 8.71848739e-02,
        1.11694678e-01, 5.60224090e-03, 3.88655462e-02, 1.17647059e-01,
        1.54061625e-02, 4.90196078e-02, 4.51680672e-02, 1.15196078e-01,
        3.50140056e-04, 2.71708683e-01, 1.27450980e-01, 4.02661064e-02,
        3.21078431e-01, 4.93697479e-02, 1.99579832e-02],
       [1.95382261e+04, 6.97701149e+00, 1.10736782e+08, 1.90734009e+01,
        4.90584232e+08, 1.00000000e+00, 4.85440613e+00, 1.19540230e+00,
        1.91954023e+00, 5.66666667e+00, 1.34022989e+01, 7.24137931e+00,
        5.36015326e+00, 3.68628739e-18, 5.44061303e-01, 6.70498084e-01,
        2.10727969e-01, 1.91570881e-02, 2.14559387e-01, 4.36781609e-01,
        1.45593870e-01, 6.59194921e-17, 2.95019157e-01, 2.95019157e-01,
        2.95019157e-01, 1.47451495e-17, 2.68199234e-02, 2.68199234e-02,
        2.49042146e-01, 1.53256705e-02, 4.98084291e-02, 8.04597701e-02,
        9.21571847e-19, 2.26053640e-01, 2.91187739e-01, 1.91570881e-02,
        3.06513410e-01, 6.13026820e-02, 7.66283525e-03]])
    
    #Drop 2 columns from the labeled_genres_new_df dataFrame
    movie_data = data[data['movieId'] == movieId].drop(columns, axis=1).to_numpy()

    #Compute distance between the movie and cluster_0
    diff0 = np.sum(np.power((movie_data - centroids[0]), 2))

    #Compute distance between the movie and cluster_1
    diff1 = np.sum(np.power((movie_data - centroids[1]), 2))
  
    #Get the label of closet cluster
    cloest_clusterLabel = np.argmin([diff0, diff1])

    #Return movies inside the closest cluster
    selected_data = data[data['clusterLabel'] == cloest_clusterLabel].drop(columns, axis=1)
  
    #Compute the cosine similarity between the movie and movies inside the closest cluster
    cos_sim = cosine_similarity(movie_data, selected_data)
    
    # Get movies indicies for tge top K most similar movies to first film.
    # [::-1] to reverse the list(min -> max), [-K] to return top similar movies, argsort: 
    # returns indices of sorted items in the list.
    neighbors_indicies = np.argsort(cos_sim[0])[-K:][::-1]
   
    for i in neighbors_indices:
        result = [data[data['clusterLabel'] == cloest_clusterLabel].iloc[i] for i in neighbors_indicies]
        
    parsed_result = []
    for item in result:
        parsed_result.append({"movieId": str(item["movieId"]), "title": item["title"], "genres": item["genres"]})

    try:
        return json.dumps(parsed_result)
    except FileNotFoundError:
        abort(404)

#Calling the function:
getNeighbors_KMeans(small_medium_large_movies_f1, 53125, 5)


if __name__ == '__main__':
   app.run(debug=True)
