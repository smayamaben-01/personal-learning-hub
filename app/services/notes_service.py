from app.repositories import notes_repository

def get_user_notes(user_id):
    return notes_repository.get_notes_by_user(user_id)

def create_note(user_id, title, content):
    if not title or not title.strip():
        raise ValueError("Title is required.")
    if len(title) > 150:
        raise ValueError("Title must be 150 characters or fewer.")
    return notes_repository.insert_note(user_id, title.strip(), content)

def update_note(note_id, user_id, title, content):
    if not title or not title.strip():
        raise ValueError("Title is required.")
    if len(title) > 150:
        raise ValueError("Title must be 150 characters or fewer.")
    return notes_repository.update_note(note_id, user_id, title.strip(), content)

def delete_note(note_id, user_id):
    return notes_repository.delete_note(note_id, user_id)