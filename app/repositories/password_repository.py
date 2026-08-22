from app.extensions import get_db_connection

def get_password_hash(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['password_hash']

def update_password_hash(user_id, new_hash):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_hash, user_id))
    conn.commit()
    cursor.close()
    conn.close()