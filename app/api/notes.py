from flask import Blueprint, request, jsonify, session
from app.decorators import login_required
from app.services import notes_service

api_note_bp = Blueprint('api_note', __name__)

@api_note_bp.route('/api/v1/notes', methods=['GET'])
@login_required
def list_notes():
    user_id = session['user_id']
    notes = notes_service.get_user_notes(user_id)
    return jsonify({"success": True, "data": notes}), 200

@api_note_bp.route('/api/v1/notes', methods=['POST'])
@login_required
def create_note():
    user_id = session['user_id']
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    try:
        note = notes_service.create_note(user_id, title, content)
        return jsonify({"success": True, "data": note}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_note_bp.route('/api/v1/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    user_id = session['user_id']
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    try:
        updated_note = notes_service.update_note(note_id, user_id, title, content)
        return jsonify({"success": True, "data": updated_note}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_note_bp.route('/api/v1/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    user_id = session['user_id']
    notes_service.delete_note(note_id, user_id)
    return jsonify({"success": True, "data": None}), 200