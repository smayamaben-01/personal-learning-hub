from app.extensions import get_db_connection

def get_topics_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dsa_topics WHERE user_id = %s", (user_id,))
    topics = cursor.fetchall()
    cursor.close()
    conn.close()
    return topics

def insert_topic(user_id, topic_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO dsa_topics (user_id, topic_name) VALUES (%s, %s)", (user_id, topic_name))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM dsa_topics WHERE id = %s", (new_id,))
    new_topic = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_topic

def update_topic(topic_id, user_id, status, questions_solved):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE dsa_topics SET status = %s, questions_solved = %s WHERE id = %s AND user_id = %s", (status, questions_solved, topic_id, user_id))
    conn.commit()
    cursor.execute("SELECT * FROM dsa_topics WHERE id = %s AND user_id = %s", (topic_id, user_id))
    updated_topic = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_topic

def delete_topic(topic_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM dsa_topics WHERE id = %s AND user_id = %s", (topic_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()