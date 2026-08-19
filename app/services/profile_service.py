from app.repositories import profile_repository
from app.utils import validation

def get_profile(user_id):
    return profile_repository.get_user_profile(user_id)

def update_profile(user_id, full_name, email, bio):
    validation.require_valid_email(email, "Email")
    validation.require_max_length(full_name, 50, "Name")
    validation.require_max_length(bio, 300, "Bio")
    return profile_repository.update_user_profile(user_id, full_name, email, bio)