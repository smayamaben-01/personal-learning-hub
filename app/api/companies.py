from flask import Blueprint, request, jsonify, session
from app.decorators import login_required
from app.services import companies_service

api_company_bp = Blueprint('api_company', __name__)

@api_company_bp.route('/api/v1/companies', methods=['GET'])
@login_required
def list_companies():
    user_id = session['user_id']
    companies = companies_service.get_user_companies(user_id)
    return jsonify({"success": True, "data": companies}), 200

@api_company_bp.route('/api/v1/companies', methods=['POST'])
@login_required
def create_company():
    user_id = session['user_id']
    data = request.get_json()
    company_name = data.get('company_name')
    status = data.get('status')
    try:
        company = companies_service.create_company(user_id, company_name, status)
        return jsonify({"success": True, "data": company}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_company_bp.route('/api/v1/companies/<int:company_id>', methods=['PUT'])
@login_required
def update_company(company_id):
    user_id = session['user_id']
    data = request.get_json()
    status = data.get('status')
    try:
        updated_company = companies_service.update_company(company_id, user_id, status)
        return jsonify({"success": True, "data": updated_company}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_company_bp.route('/api/v1/companies/<int:company_id>', methods=['DELETE'])
@login_required
def delete_company(company_id):
    user_id = session['user_id']
    companies_service.delete_company(company_id, user_id)
    return jsonify({"success": True, "data": None}), 200