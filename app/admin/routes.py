from flask import Blueprint, jsonify, session, request
from app.db import connect_db_api
from functools import wraps

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
def admin_list():
    conn = connect_db_api()
    cursor = conn.cursor()

    cursor.execute('SELECT id, username, role FROM admin')
    admins = [{"id": row[0], "username": row[1], "role": row[2]} for row in cursor.fetchall()]

    conn.close()
    return jsonify(admins)


@admin_bp.route("/delete", methods=["DELETE"])
@main_admin_required
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
