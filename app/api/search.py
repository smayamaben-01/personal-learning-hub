from flask import Blueprint, request, jsonify, session
from app.decorators import login_required
from app.services import search_service

api_search_bp = Blueprint('api_search', __name__)

@api_search_bp.route('/api/v1/search', methods=['GET'])
@login_required
def get_search_query():
    keyword = request.args.get('q')
    search_type = request.args.get('type', 'all')
    try:
        search_query = search_service.search_all(session['user_id'], keyword, search_type)
        return jsonify({"success": True, "data": search_query}), 200
    except ValueError as e:
          return jsonify({"success": False, "error": str(e)}), 400