from flask import Blueprint, request, jsonify, session
from app.decorators import login_required
from app.services import password_service

api_password_bp = Blueprint('api_password', __name__)

@api_password_bp.route('/api/v1/profile/password', methods=['PUT'])
@login_required
def change_password():
    user_id = session['user_id']
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    try:
        password_service.change_password(user_id, current_password, new_password)
        return jsonify({"success": True, "data": "Password updated successfully."}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400