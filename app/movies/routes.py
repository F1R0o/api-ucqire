from flask import Blueprint, request, jsonify
from app.db import connect_db_api
from flasgger import swag_from

movies_bp = Blueprint('movies_bp', __name__)

@movies_bp.route("/by-id", methods=["GET"])
@movies_bp.route("/by-id", methods=["GET"])
@swag_from({
    'tags': ['Movies'],
    'description': 'Get a movie by its ID.',
    'parameters': [
        {'name': 'id', 'in': 'query', 'type': 'integer', 'description': 'Movie ID', 'required': True}
    ],
    'responses': {
        200: {'description': 'Movie details'},
        400: {'description': 'Invalid or missing ID'}
    }
})
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
@movies_bp.route("/all", methods=["GET"])
@swag_from({
    'tags': ['Movies'],
    'description': 'Get a paginated list of all movies',
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'description': 'Page number',
            'required': False
        }
    ],
    'responses': {
        200: {
            'description': 'A list of movies',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object'
                }
            }
        }
    }
})
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
@swag_from({
    'tags': ['Movies'],
    'description': 'Search movies by genre.',
    'parameters': [
        {'name': 'genre', 'in': 'query', 'type': 'string', 'description': 'Genre of the movies to search for', 'required': True}
    ],
    'responses': {
        200: {'description': 'Matching movies found', 'content': {'application/json': {}}},
        400: {'description': 'Genre is required', 'content': {'application/json': {}}},
        500: {'description': 'Internal server error', 'content': {'application/json': {}}}
    }
})
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
@swag_from({
    'tags': ['Movies'],
    'description': 'Search movies by title.',
    'parameters': [
        {'name': 'query', 'in': 'query', 'type': 'string', 'description': 'Movie title to search', 'required': True}
    ],
    'responses': {
        200: {'description': 'Matching movies'}
    }
})
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
@swag_from({
    'tags': ['Movies'],
    'description': 'Get the most viewed movies.',
    'responses': {
        200: {'description': 'List of most viewed movies'}
    }
})
def most_viewed_movies():
    conn = connect_db_api()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies ORDER BY views DESC LIMIT 54")
    columns = [col[0] for col in cursor.description]
    movies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(movies)


@movies_bp.route("/latest", methods=["GET"])
@swag_from({
    'tags': ['Movies'],
    'description': 'Get the latest movies added.',
    'responses': {
        200: {'description': 'List of latest movies'}
    }
})
def latest_movies():
    conn = connect_db_api()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies ORDER BY id DESC LIMIT 54")
    columns = [col[0] for col in cursor.description]
    movies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(movies)
