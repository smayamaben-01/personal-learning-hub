from flask import Blueprint, jsonify, session
from app.decorators import login_required
from app.services import dashboard_service

api_dashboard_bp = Blueprint('api_dashboard', __name__)

@api_dashboard_bp.route('/api/v1/dashboard/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    stats = dashboard_service.get_dashboard_stats(session['user_id'])
    return jsonify({"success": True, "data": stats})