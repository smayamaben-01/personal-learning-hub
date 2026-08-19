from flask import Blueprint, request, jsonify, session
from app.decorators import login_required
from app.services import profile_service

api_profile_bp = Blueprint('api_profile', __name__)

@api_profile_bp.route('/api/v1/profile', methods=['GET'])
@login_required
def get_user_profile():
    user_id = session['user_id']
    profiles = profile_service.get_profile(user_id)
    return jsonify({"success": True, "data": profiles}), 200

@api_profile_bp.route('/api/v1/profile', methods=['PUT'])
@login_required
def update_user_profile():
    user_id = session['user_id']
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    bio = data.get('bio')
    try:
        updated_profile = profile_service.update_profile(user_id, full_name, email, bio)
        return jsonify({"success": True, "data": updated_profile}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        if 'Duplicate entry' in str(e):
            return jsonify({"success": False, "error": "Email already in use."}), 409
        raise