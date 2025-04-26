from flask import Blueprint, jsonify, session, request
from app.db import connect_db_api
from functools import wraps
from flasgger import swag_from
admin_bp = Blueprint('admin_bp', __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

def main_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'main_admin':
            return jsonify({"error": "Forbidden"}), 403
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/stats", methods=["GET"])
@admin_required
@swag_from({
    'tags': ['Admin'],
    'description': 'Get the site statistics, including total movies and TV series.',
    'responses': {
        200: {
            'description': 'Site statistics retrieved successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'total_movies': {'type': 'integer', 'description': 'Total number of movies in the database'},
                            'total_series': {'type': 'integer', 'description': 'Total number of TV series in the database'}
                        }
                    }
                }
            }
        },
        500: {'description': 'Internal server error', 'content': {'application/json': {}}}
    }
})
def site_stats():
    conn = connect_db_api()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM movies')
    total_movies = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tv_series')
    total_series = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "total_movies": total_movies,
        "total_series": total_series
    })


@admin_bp.route("/list", methods=["GET"])
@main_admin_required
@swag_from({
    'tags': ['Admin'],
    'description': 'Get a list of all admins with their usernames and roles.',
    'responses': {
        200: {
            'description': 'Admin list retrieved successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'description': 'Admin ID'},
                                'username': {'type': 'string', 'description': 'Admin username'},
                                'role': {'type': 'string', 'description': 'Admin role'}
                            }
                        }
                    }
                }
            }
        },
        500: {'description': 'Internal server error', 'content': {'application/json': {}}}
    }
})
def admin_list():
    conn = connect_db_api()
    cursor = conn.cursor()

    cursor.execute('SELECT id, username, role FROM admin')
    admins = [{"id": row[0], "username": row[1], "role": row[2]} for row in cursor.fetchall()]

    conn.close()
    return jsonify(admins)


@admin_bp.route("/delete", methods=["DELETE"])
@main_admin_required
@swag_from({
    'tags': ['Admin'],
    'description': 'Delete an admin account.',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'admin_id': {'type': 'integer', 'description': 'ID of the admin to be deleted'}
                    },
                    'required': ['admin_id']
                }
            }
        }
    },
    'responses': {
        200: {'description': 'Admin deleted successfully', 'content': {'application/json': {}}},
        400: {'description': 'Missing admin_id in request', 'content': {'application/json': {}}},
        403: {'description': 'Cannot delete main admin', 'content': {'application/json': {}}},
        404: {'description': 'Admin not found', 'content': {'application/json': {}}},
        500: {'description': 'Internal server error', 'content': {'application/json': {}}}
    }
})
def delete_admin():
    admin_id = request.json.get('admin_id')

    if not admin_id:
        return jsonify({"error": "admin_id required"}), 400

    conn = connect_db_api()
    cursor = conn.cursor()

    
    cursor.execute('SELECT role FROM admin WHERE id=?', (admin_id,))
    admin = cursor.fetchone()

    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    if admin[0] == "main_admin":
        return jsonify({"error": "Cannot delete main admin"}), 403

    cursor.execute('DELETE FROM admin WHERE id=?', (admin_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Admin deleted successfully"}), 200
