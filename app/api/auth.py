from flask import Blueprint, request, jsonify, session
from app.services import auth_service

api_auth_bp = Blueprint('api_auth', __name__)

@api_auth_bp.route('/api/v1/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    try:
        user_id = auth_service.register_user(username, password)
        return jsonify({"success": True, "data": {"id": user_id, "username": username}}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    try:
        user = auth_service.authenticate_user(username, password)
        session['user_id'] = user['id']
        return jsonify({"success": True, "data": {"id": user['id'], "username": user['username']}}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 401

@api_auth_bp.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True, "data": None}), 200

@api_auth_bp.route('/api/v1/auth/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401
    return jsonify({"success": True, "data": {"id": session['user_id']}}), 200