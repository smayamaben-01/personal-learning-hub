from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories import auth_repository
from app.utils import validation

def register_user(username, password):
    validation.require_non_empty(username, "Username")
    validation.require_max_length(username, 50, "Username")
    validation.require_non_empty(password, "Password")

    existing = auth_repository.get_user_by_username(username)
    if existing:
        raise ValueError("That username is already taken.")

    hashed = generate_password_hash(password)
    user_id = auth_repository.create_user(username, hashed)
    return user_id

def authenticate_user(username, password):
    user = auth_repository.get_user_by_username(username)
    if not user or not check_password_hash(user['password_hash'], password):
        raise ValueError("Invalid username or password.")
    return user