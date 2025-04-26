from flask import Blueprint, request, jsonify
from app.db import connect_db_api


movies_bp = Blueprint('movies_bp', __name__)

@movies_bp.route("/by-id", methods=["GET"])
def by_id_movie():
    id_param = request.args.get("id")
    if not id_param or not id_param.isdigit():
        return jsonify({"error": "Invalid or missing id parameter"}), 400

    conn = connect_db_api()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE id=?", (int(id_param),))
    columns = [col[0] for col in cursor.description]
    movie = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(movie)


@movies_bp.route("/all", methods=["GET"])
def all_movies():
    conn = connect_db_api()
    cursor = conn.cursor()

    page = int(request.args.get('page', 1))
    items_per_page = 54
    offset = (page - 1) * items_per_page

    cursor.execute('SELECT * FROM movies LIMIT ? OFFSET ?', (items_per_page, offset))
    columns = [col[0] for col in cursor.description]
    movies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(movies)


@movies_bp.route("/by-genre", methods=["GET"])
def movies_by_genre():
    genre = request.args.get('genre')
    if not genre:
        return jsonify({"error": "Genre is required"}), 400

    conn = connect_db_api()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE genres LIKE ?", ('%' + genre + '%',))
    columns = [col[0] for col in cursor.description]
    movies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(movies)


@movies_bp.route("/search", methods=["GET"])
def search_movies():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400

    conn = connect_db_api()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE title_eng LIKE ?", ('%' + query + '%',))
    columns = [col[0] for col in cursor.description]
    movies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(movies)


@movies_bp.route("/most-viewed", methods=["GET"])
def most_viewed_movies():
    conn = connect_db_api()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies ORDER BY views DESC LIMIT 54")
    columns = [col[0] for col in cursor.description]
    movies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(movies)


@movies_bp.route("/latest", methods=["GET"])
def latest_movies():
    conn = connect_db_api()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies ORDER BY id DESC LIMIT 54")
    columns = [col[0] for col in cursor.description]
    movies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(movies)
