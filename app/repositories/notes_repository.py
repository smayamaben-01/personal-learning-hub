from app.extensions import get_db_connection

def get_notes_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE user_id = %s", (user_id,))
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return notes

def insert_note(user_id, title, content):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)", (user_id, title, content))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM notes WHERE id = %s", (new_id,))
    new_note = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_note

def update_note(note_id, user_id, title, content):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s AND user_id = %s", (title, content, note_id, user_id))
    conn.commit()
    cursor.execute("SELECT * FROM notes WHERE id = %s AND user_id = %s", (note_id, user_id))
    updated_note = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_note

def delete_note(note_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM notes WHERE id = %s AND user_id = %s", (note_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()