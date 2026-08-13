from app.repositories import dsa_repository

def get_user_topics(user_id):
    return dsa_repository.get_topics_by_user(user_id)

def create_topic(user_id, topic_name):
    if not topic_name or not topic_name.strip():
        raise ValueError("Topic name is required.")
    if len(topic_name) > 100:
        raise ValueError("Topic name must be 100 characters or fewer.")
    return dsa_repository.insert_topic(user_id, topic_name.strip())

VALID_STATUSES = ['Not Started', 'In Progress', 'Completed']

def update_topic(topic_id, user_id, status, questions_solved):
    if status not in VALID_STATUSES:
        raise ValueError("Invalid status value.")
    questions_solved = int(questions_solved)
    if questions_solved < 0:
        raise ValueError("Questions solved cannot be negative.")
    return dsa_repository.update_topic(topic_id, user_id, status, questions_solved)

def delete_topic(topic_id, user_id):
    return dsa_repository.delete_topic(topic_id, user_id)