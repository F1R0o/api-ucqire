from flask import Blueprint, request, jsonify
from app.db import connect_db_api2
from flasgger import swag_from
from app.extensions import cache

series_bp = Blueprint('series_bp', __name__)


@series_bp.route("/all", methods=["GET"])
@cache.cached(timeout=60)
@swag_from({
    'tags': ['Series'],
    'description': 'Get a paginated list of all TV series.',
    'parameters': [
        {'name': 'page', 'in': 'query', 'type': 'integer', 'description': 'Page number', 'required': False}
    ],
    'responses': {
        200: {'description': 'List of TV series'}
    }
})
def all_series():
    conn = connect_db_api2()
    cursor = conn.cursor()

    page = int(request.args.get('page', 1))
    items_per_page = 54
    offset = (page - 1) * items_per_page

    cursor.execute('SELECT * FROM tv_series LIMIT ? OFFSET ?', (items_per_page, offset))
    columns = [col[0] for col in cursor.description]
    series_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(series_list)


@series_bp.route("/by-id", methods=["GET"])
@swag_from({
    'tags': ['Series'],
    'description': 'Get a TV series by its ID.',
    'parameters': [
        {'name': 'id', 'in': 'query', 'type': 'integer', 'description': 'Series ID', 'required': True}
    ],
    'responses': {
        200: {'description': 'Series details'},
        400: {'description': 'Invalid or missing ID'}
    }
})
def series_by_id():
    id_param = request.args.get("id")
    if not id_param or not id_param.isdigit():
        return jsonify({"error": "Invalid or missing id parameter"}), 400

    conn = connect_db_api2()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tv_series WHERE id=?", (int(id_param),))
    columns = [col[0] for col in cursor.description]
    series = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(series)


@series_bp.route("/episodes", methods=["GET"])
@cache.cached(timeout=60)
@swag_from({
    'tags': ['Series'],
    'description': 'Get episodes for a series',
    'parameters': [
        {
            'name': 'series_id',
            'in': 'query',
            'type': 'integer',
            'required': True,
            'description': 'ID of the TV series'
        }
    ],
    'responses': {
        200: {
            'description': 'List of episodes'
        },
        400: {
            'description': 'Invalid series ID'
        }
    }
})
def series_episodes():
    series_id = request.args.get("series_id")
    if not series_id or not series_id.isdigit():
        return jsonify({"error": "Invalid or missing series_id parameter"}), 400

    conn = connect_db_api2()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM episodes WHERE series_id=?", (int(series_id),))
    columns = [col[0] for col in cursor.description]
    episodes = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(episodes)


@series_bp.route("/search", methods=["GET"])
@swag_from({
    'tags': ['Series'],
    'description': 'Search TV series by title.',
    'parameters': [
        {'name': 'query', 'in': 'query', 'type': 'string', 'description': 'TV series title to search for', 'required': True}
    ],
    'responses': {
        200: {'description': 'Matching TV series found', 'content': {'application/json': {}}},
        400: {'description': 'Query is required', 'content': {'application/json': {}}},
        500: {'description': 'Internal server error', 'content': {'application/json': {}}}
    }
})
def search_series():

    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400

    conn = connect_db_api2()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tv_series WHERE title_eng LIKE ?", ('%' + query + '%',))
    columns = [col[0] for col in cursor.description]
    series_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(series_list)


@series_bp.route("/most-viewed", methods=["GET"])
@swag_from({
    'tags': ['Series'],
    'description': 'Get the most viewed TV series.',
    'responses': {
        200: {'description': 'Most viewed TV series list', 'content': {'application/json': {}}},
        500: {'description': 'Internal server error', 'content': {'application/json': {}}}
    }
})
def most_viewed_series():
    conn = connect_db_api2()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tv_series ORDER BY views DESC LIMIT 54")
    columns = [col[0] for col in cursor.description]
    series_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(series_list)


@series_bp.route("/latest", methods=["GET"])
@swag_from({
    'tags': ['Series'],
    'description': 'Get the latest TV series.',
    'responses': {
        200: {'description': 'Latest TV series list', 'content': {'application/json': {}}},
        500: {'description': 'Internal server error', 'content': {'application/json': {}}}
    }
})
def latest_series():
    conn = connect_db_api2()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tv_series ORDER BY id DESC LIMIT 54")
    columns = [col[0] for col in cursor.description]
    series_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(series_list)
