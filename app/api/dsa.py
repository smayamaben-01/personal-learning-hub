from flask import Blueprint, request, jsonify, session
from app.decorators import login_required
from app.services import dsa_service

api_dsa_bp = Blueprint('api_dsa', __name__)

@api_dsa_bp.route('/api/v1/dsa-topics', methods=['GET'])
@login_required
def list_topics():
    user_id = session['user_id']
    topics = dsa_service.get_user_topics(user_id)
    return jsonify({"success": True, "data": topics}), 200

@api_dsa_bp.route('/api/v1/dsa-topics', methods=['POST'])
@login_required
def create_topic():
    user_id = session['user_id']
    data = request.get_json()
    try:
        topic = dsa_service.create_topic(user_id, data.get('topic_name'))
        return jsonify({"success": True, "data": topic}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_dsa_bp.route('/api/v1/dsa-topics/<int:topic_id>', methods=['PUT'])
@login_required
def update_topic(topic_id):
    user_id = session['user_id']
    data = request.get_json()
    status = data.get('status')
    questions_solved = data.get('questions_solved')
    try:
        updated_topic = dsa_service.update_topic(topic_id, user_id, status, questions_solved)
        return jsonify({"success": True, "data": updated_topic}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_dsa_bp.route('/api/v1/dsa-topics/<int:topic_id>', methods=['DELETE'])
@login_required
def delete_topic(topic_id):
    user_id = session['user_id']
    dsa_service.delete_topic(topic_id, user_id)
    return jsonify({"success": True, "data": None}), 200