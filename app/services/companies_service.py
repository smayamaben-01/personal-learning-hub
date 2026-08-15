from app.repositories import companies_repository
from app.utils import validation

def get_user_companies(user_id):
    return companies_repository.get_companies_by_user(user_id)

VALID_STATUSES = ['Applied', 'OA', 'Interview', 'Rejected', 'Selected']

def create_company(user_id, company_name, status):
    validation.require_non_empty(company_name, "Company name")
    validation.require_max_length(company_name, 100, "Company name")
    validation.require_one_of(status, VALID_STATUSES, "status")
    return companies_repository.insert_company(user_id, company_name.strip(), status)

def update_company(company_id, user_id, status):
    validation.require_one_of(status, VALID_STATUSES, "status")
    return companies_repository.update_company(company_id, user_id, status)

def delete_company(company_id, user_id):
    return companies_repository.delete_company(company_id, user_id)