from app.extensions import get_db_connection

def search_dsa_topics(user_id, keyword):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    pattern = f"%{keyword}%"
    cursor.execute("SELECT * FROM dsa_topics WHERE user_id = %s AND topic_name LIKE %s", (user_id, pattern))
    matching_topic = cursor.fetchall()
    cursor.close()
    conn.close()
    return matching_topic

def search_companies(user_id, keyword):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    pattern = f"%{keyword}%"
    cursor.execute("SELECT * FROM companies WHERE user_id = %s AND company_name LIKE %s", (user_id, pattern))
    matching_name = cursor.fetchall()
    cursor.close()
    conn.close()
    return matching_name

def search_notes(user_id, keyword):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    pattern = f"%{keyword}%"
    cursor.execute("SELECT * FROM notes WHERE user_id = %s AND (title LIKE %s OR content LIKE %s)", (user_id, pattern, pattern))
    matching_note = cursor.fetchall()
    cursor.close()
    conn.close()
    return matching_note