from flask import Blueprint, request, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import connect_db_api
from functools import wraps
from flasgger import swag_from
auth_bp = Blueprint('auth_bp', __name__)



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



@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Login an admin user with username and password.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'Login successful'},
        401: {'description': 'Invalid credentials'},
        404: {'description': 'User not found'}
    }
})
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = connect_db_api()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_id, username_db, password_hash_db, role, *permissions = user

        if check_password_hash(password_hash_db, password):
            session['logged_in'] = True
            session['username'] = username_db
            session['role'] = role

            
            permission_names = [
                'can_upload_movie', 'can_edit_movie', 'can_delete_movie',
                'can_view_analytics', 'can_view_admin_list',
                'can_manage_sponsors', 'can_upload_sliders'
            ]
            for idx, perm in enumerate(permission_names):
                session[perm] = bool(permissions[idx])

            return jsonify({"message": "Logged in successfully"}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404

@auth_bp.route('/logout')
@swag_from({
    'tags': ['Authentication'],
    'description': 'Logout the currently logged-in admin.',
    'responses': {
        200: {'description': 'Logged out successfully'}
    }
})
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/setup_main_admin', methods=["POST"])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Setup the first main admin (only once).',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'Main admin created successfully'},
        400: {'description': 'Main admin already exists'}
    }
})
def setup_main_admin():
    username = request.json.get('username')
    password = request.json.get('password')

    conn = connect_db_api()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM admin WHERE role="main_admin"')
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Main admin already exists"}), 400

    password_hash = generate_password_hash(password)
    cursor.execute('''
        INSERT INTO admin (username, password_hash, role,
            can_upload_movie, can_edit_movie, can_delete_movie,
            can_view_analytics, can_view_admin_list,
            can_manage_sponsors, can_upload_sliders)
        VALUES (?, ?, ?, 1, 1, 1, 1, 1, 1, 1)
    ''', (username, password_hash, 'main_admin'))

    conn.commit()
    conn.close()

    return jsonify({"message": "Main admin created successfully"}), 201

@auth_bp.route('/create_admin', methods=["POST"])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Create a new admin (only by main_admin).',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                    'can_upload_movie': {'type': 'boolean'},
                    'can_edit_movie': {'type': 'boolean'},
                    'can_delete_movie': {'type': 'boolean'},
                    'can_view_analytics': {'type': 'boolean'},
                    'can_view_admin_list': {'type': 'boolean'},
                    'can_manage_sponsors': {'type': 'boolean'},
                    'can_upload_sliders': {'type': 'boolean'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'Admin created successfully'},
        403: {'description': 'Only main admin can create new admins'}
    }
})
@main_admin_required
def create_admin():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    permissions = {
        'can_upload_movie': data.get('can_upload_movie', False),
        'can_edit_movie': data.get('can_edit_movie', False),
        'can_delete_movie': data.get('can_delete_movie', False),
        'can_view_analytics': data.get('can_view_analytics', False),
        'can_view_admin_list': data.get('can_view_admin_list', False),
        'can_manage_sponsors': data.get('can_manage_sponsors', False),
        'can_upload_sliders': data.get('can_upload_sliders', False),
    }

    password_hash = generate_password_hash(password)

    conn = connect_db_api()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO admin (username, password_hash, role,
            can_upload_movie, can_edit_movie, can_delete_movie,
            can_view_analytics, can_view_admin_list,
            can_manage_sponsors, can_upload_sliders)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        username, password_hash, 'admin',
        permissions['can_upload_movie'],
        permissions['can_edit_movie'],
        permissions['can_delete_movie'],
        permissions['can_view_analytics'],
        permissions['can_view_admin_list'],
        permissions['can_manage_sponsors'],
        permissions['can_upload_sliders'],
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Admin created successfully"}), 201
