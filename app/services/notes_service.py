from app.repositories import notes_repository
from app.utils import validation, render

def get_user_notes(user_id):
    notes = notes_repository.get_notes_by_user(user_id)
    for note in notes:
        note['rendered_content'] = render.render_note_content(note['content'])
    return notes

def create_note(user_id, title, content):
    validation.require_non_empty(title, "Title")
    validation.require_max_length(title, 150, "Title")
    return notes_repository.insert_note(user_id, title.strip(), content)

def update_note(note_id, user_id, title, content):
    validation.require_non_empty(title, "Title")
    validation.require_max_length(title, 150, "Title")
    return notes_repository.update_note(note_id, user_id, title.strip(), content)

def delete_note(note_id, user_id):
    return notes_repository.delete_note(note_id, user_id)