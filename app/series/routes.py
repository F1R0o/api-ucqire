from flask import Blueprint, request, jsonify
from app.db import connect_db_api2

series_bp = Blueprint('series_bp', __name__)


@series_bp.route("/all", methods=["GET"])
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
def most_viewed_series():
    conn = connect_db_api2()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tv_series ORDER BY views DESC LIMIT 54")
    columns = [col[0] for col in cursor.description]
    series_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(series_list)


@series_bp.route("/latest", methods=["GET"])
def latest_series():
    conn = connect_db_api2()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tv_series ORDER BY id DESC LIMIT 54")
    columns = [col[0] for col in cursor.description]
    series_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(series_list)
