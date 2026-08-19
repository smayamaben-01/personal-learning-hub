from app.extensions import get_db_connection

def get_user_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, full_name, email, bio, updated_at FROM users WHERE id = %s", (user_id,))
    profile = cursor.fetchone()
    cursor.close()
    conn.close()
    return profile

def update_user_profile(user_id, full_name, email, bio):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE users SET full_name = %s, email = %s, bio = %s WHERE id = %s", (full_name, email, bio, user_id))
    conn.commit()
    cursor.execute("SELECT id, username, full_name, email, bio, updated_at FROM users WHERE id = %s", (user_id,))
    updated_profile = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_profile