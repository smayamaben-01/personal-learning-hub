from flask import Blueprint, request, jsonify, session
from app.decorators import login_required
from app.services import goals_service

api_goals_bp = Blueprint('api_goals', __name__)

@api_goals_bp.route('/api/v1/goals', methods=['GET'])
@login_required
def list_goals():
    user_id = session['user_id']
    goals = goals_service.get_current_week_goals(user_id)
    return jsonify({"success": True, "data": goals}), 200

@api_goals_bp.route('/api/v1/goals', methods=['POST'])
@login_required
def create_goal():
    user_id = session['user_id']
    data = request.get_json()
    description = data.get('description')
    target_count = data.get('target_count')
    try:
        goal = goals_service.add_goal(user_id, description, target_count)
        return jsonify({"success": True, "data": goal}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_goals_bp.route('/api/v1/goals/<int:goal_id>', methods=['PUT'])
@login_required
def update_goal(goal_id):
    user_id = session['user_id']
    data = request.get_json()
    current_count = data.get('current_count')
    try:
        updated_goal = goals_service.increment_goal_progress(goal_id, user_id, current_count)
        if updated_goal is None:
            return jsonify({"success": False, "error": "Goal not found"}), 404
        return jsonify({"success": True, "data": updated_goal}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_goals_bp.route('/api/v1/goals/<int:goal_id>', methods=['DELETE'])
@login_required
def delete_goal(goal_id):
    user_id = session['user_id']
    deleted = goals_service.remove_goal(goal_id, user_id)
    if not deleted:
        return jsonify({"success": False, "error": "Goal not found"}), 404
    return jsonify({"success": True, "data": None}), 200