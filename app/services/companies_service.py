from app.repositories import companies_repository

def get_user_companies(user_id):
    return companies_repository.get_companies_by_user(user_id)

VALID_STATUSES = ['Applied', 'OA', 'Interview', 'Rejected', 'Selected']

def create_company(user_id, company_name, status):
    if not company_name or not company_name.strip():
        raise ValueError("Company name is required.")
    if len(company_name) > 100:
        raise ValueError("Company name must be 100 characters or fewer.")
    if status not in VALID_STATUSES:
            raise ValueError("Invalid status value.")
    return companies_repository.insert_company(user_id, company_name.strip(), status)

def update_company(company_id, user_id, status):
    if status not in VALID_STATUSES:
        raise ValueError("Invalid status value.")
    return companies_repository.update_company(company_id, user_id, status)

def delete_company(company_id, user_id):
    return companies_repository.delete_company(company_id, user_id)