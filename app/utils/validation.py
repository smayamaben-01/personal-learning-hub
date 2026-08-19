import re

def require_non_empty(value, field_name):
     if not value or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

def require_one_of(value, allowed_values, field_name):
      if value not in allowed_values:
            raise ValueError(f"Invalid {field_name} value.")

def require_max_length(value, max_length, field_name):
      if len(value) > max_length:
            raise ValueError(f"{field_name} must be {max_length} characters or fewer.")

def require_min_length(value, min_length, field_name):
      if len(value) < min_length:
            raise ValueError(f"{field_name} must have {min_length} characters or more.")

def require_valid_email(value, field_name):
    if value and not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', value):
        raise ValueError(f"{field_name} must be a valid email address.")