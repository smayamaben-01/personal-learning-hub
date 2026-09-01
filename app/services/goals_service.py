from app.repositories import goals_repository
from app.utils import validation
from datetime import date, timedelta

def get_week_start():
    today = date.today()
    return today - timedelta(days=today.weekday())

def get_current_week_goals(user_id):
    week_start_date = get_week_start()
    return goals_repository.get_goals_for_user(user_id, week_start_date)

def add_goal(user_id, description, target_count):
    validation.require_non_empty(description, "Description")
    validation.require_max_length(description, 255, "Description")
    target_count = int(target_count)
    validation.require_positive_int(target_count, "Target count")
    week_start_date = get_week_start()
    return goals_repository.create_goal(user_id, description.strip(), target_count, week_start_date)

def increment_goal_progress(goal_id, user_id, current_count):
    current_count = int(current_count)
    if current_count < 0:
        raise ValueError("Goal count cannot be negative.")
    return goals_repository.update_goal_progress(goal_id, user_id, current_count)

def remove_goal(goal_id, user_id):
    return goals_repository.delete_goal(goal_id, user_id)