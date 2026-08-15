from app.repositories import dsa_repository
from app.utils import validation

def get_user_topics(user_id):
    return dsa_repository.get_topics_by_user(user_id)

def create_topic(user_id, topic_name):
    validation.require_non_empty(topic_name, "Topic name")
    validation.require_max_length(topic_name, 100, "Topic name")
    return dsa_repository.insert_topic(user_id, topic_name.strip())

VALID_STATUSES = ['Not Started', 'In Progress', 'Completed']

def update_topic(topic_id, user_id, status, questions_solved):
    validation.require_one_of(status, VALID_STATUSES, "status")
    questions_solved = int(questions_solved)
    if questions_solved < 0:
        raise ValueError("Questions solved cannot be negative.")
    return dsa_repository.update_topic(topic_id, user_id, status, questions_solved)

def delete_topic(topic_id, user_id):
    return dsa_repository.delete_topic(topic_id, user_id)