from flask import Blueprint, request, jsonify, session
from app.db import connect_db_api, connect_db_api2
from functools import wraps
from flasgger import swag_from
upload_bp = Blueprint('upload_bp', __name__)


def admin_upload_permission_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not (session.get('can_upload_movie', False) or session.get('role') == 'main_admin'):
            return jsonify({"error": "No permission to upload"}), 403
        return f(*args, **kwargs)
    return decorated_function


@upload_bp.route("/movie", methods=["POST"])
@swag_from({
    'tags': ['Upload'],
    'description': 'Upload a new movie to the platform.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'title_eng': {'type': 'string'},
                    'imdb': {'type': 'string'},
                    'year': {'type': 'integer'},
                    'genres': {'type': 'string'},
                    'poster': {'type': 'string'},
                    'description': {'type': 'string'}
                },
                'required': ['title_eng', 'imdb', 'year', 'genres', 'poster']
            }
        }
    ],
    'responses': {
        201: {'description': 'Movie uploaded successfully'},
        400: {'description': 'Missing required fields'}
    }
})
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
@swag_from({
    'tags': ['Upload'],
    'description': 'Upload a new TV series.',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title_eng': {'type': 'string', 'description': 'English title of the TV series'},
                        'imdb': {'type': 'string', 'description': 'IMDb rating of the series'},
                        'year': {'type': 'integer', 'description': 'Year of release'},
                        'genres': {'type': 'string', 'description': 'Genres of the series'},
                        'poster': {'type': 'string', 'description': 'Link to the poster image'},
                        'description': {'type': 'string', 'description': 'Description of the series'}
                    },
                    'required': ['title_eng', 'imdb', 'year', 'genres', 'poster']
                }
            }
        }
    },
    'responses': {
        201: {'description': 'Series uploaded successfully', 'content': {'application/json': {}}},
        400: {'description': 'Missing fields', 'content': {'application/json': {}}},
        500: {'description': 'Internal server error', 'content': {'application/json': {}}}
    }
})
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
@swag_from({
    'tags': ['Upload'],
    'description': 'Upload a new episode for a TV series.',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'series_id': {'type': 'integer', 'description': 'ID of the series'},
                        'title_eng': {'type': 'string', 'description': 'Title of the episode'},
                        'season': {'type': 'integer', 'description': 'Season number'},
                        'episode_number': {'type': 'integer', 'description': 'Episode number'},
                        'video_link': {'type': 'string', 'description': 'Link to the episode video'}
                    },
                    'required': ['series_id', 'title_eng', 'season', 'episode_number', 'video_link']
                }
            }
        }
    },
    'responses': {
        201: {'description': 'Episode uploaded successfully', 'content': {'application/json': {}}},
        400: {'description': 'Missing fields', 'content': {'application/json': {}}},
        500: {'description': 'Internal server error', 'content': {'application/json': {}}}
    }
})
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
