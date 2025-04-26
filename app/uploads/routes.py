from flask import Blueprint, request, jsonify, session
from app.db import connect_db_api, connect_db_api2
from functools import wraps

upload_bp = Blueprint('upload_bp', __name__)


def admin_upload_permission_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not (session.get('can_upload_movie', False) or session.get('role') == 'main_admin'):
            return jsonify({"error": "No permission to upload"}), 403
        return f(*args, **kwargs)
    return decorated_function


@upload_bp.route("/movie", methods=["POST"])
@admin_upload_permission_required
def upload_movie():
    data = request.json
    title_eng = data.get('title_eng')
    imdb = data.get('imdb')
    year = data.get('year')
    genres = data.get('genres')
    poster = data.get('poster')
    description = data.get('description')

    if not all([title_eng, imdb, year, genres, poster]):
        return jsonify({"error": "Missing fields"}), 400

    conn = connect_db_api()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO movies (title_eng, imdb, year, genres, poster, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title_eng, imdb, year, genres, poster, description))
    conn.commit()
    conn.close()

    return jsonify({"message": "Movie uploaded successfully"}), 201


@upload_bp.route("/series", methods=["POST"])
@admin_upload_permission_required
def upload_series():
    data = request.json
    title_eng = data.get('title_eng')
    imdb = data.get('imdb')
    year = data.get('year')
    genres = data.get('genres')
    poster = data.get('poster')
    description = data.get('description')

    if not all([title_eng, imdb, year, genres, poster]):
        return jsonify({"error": "Missing fields"}), 400

    conn = connect_db_api2()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tv_series (title_eng, imdb, year, genres, poster, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title_eng, imdb, year, genres, poster, description))
    conn.commit()
    conn.close()

    return jsonify({"message": "Series uploaded successfully"}), 201


@upload_bp.route("/episode", methods=["POST"])
@admin_upload_permission_required
def upload_episode():
    data = request.json
    series_id = data.get('series_id')
    title_eng = data.get('title_eng')
    season = data.get('season')
    episode_number = data.get('episode_number')
    video_link = data.get('video_link')

    if not all([series_id, title_eng, season, episode_number, video_link]):
        return jsonify({"error": "Missing fields"}), 400

    conn = connect_db_api2()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO episodes (series_id, title_eng, season, episode_number, video_link)
        VALUES (?, ?, ?, ?, ?)
    ''', (series_id, title_eng, season, episode_number, video_link))
    conn.commit()
    conn.close()

    return jsonify({"message": "Episode uploaded successfully"}), 201
