from app.repositories import password_repository
from app.utils import validation
from werkzeug.security import generate_password_hash, check_password_hash

def change_password(user_id, current_password, new_password):
    old_password = password_repository.get_password_hash(user_id)
    if check_password_hash(old_password, current_password):
        validation.require_min_length(new_password, 8, "Password")
        new_hashed_password = generate_password_hash(new_password)
        password_repository.update_password_hash(user_id, new_hashed_password)
    else:
        raise ValueError("Current password is incorrect.")