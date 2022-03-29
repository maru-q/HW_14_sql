from flask import Flask, jsonify
from sql_functions import search_by_title, search_by_year_range, search_by_raiting, search_by_genre

app = Flask(__name__)


@app.route("/movie/<title>")
def search_film_page(title):
    data = search_by_title(title)
    return jsonify(data)


@app.route("/movie/<int:year_start>/to/<int:year_end>")
def search_film_by_range(year_start, year_end):
    data = search_by_year_range(year_start, year_end)
    return jsonify(data)


@app.route("/rating/children")
def movies_for_children():
    raiting_list = ["G"]
    movies = search_by_raiting(raiting_list)
    return jsonify(movies)


@app.route("/rating/family")
def movies_for_family():
    raiting_list = ["G", "PG", "PG-13"]
    movies = search_by_raiting(raiting_list)
    return jsonify(movies)


@app.route("/rating/adult")
def movies_for_adult():
    raiting_list = ["R", "NC-17"]
    movies = search_by_raiting(raiting_list)
    return jsonify(movies)


@app.route("/genre/<genre>")
def films_by_genre(genre):
    movies = search_by_genre(genre)
    return jsonify(movies)


if __name__ == "__main__":
    app.run()
