from app.extensions import get_db_connection

def get_topics_by_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT status, COUNT(*) AS count FROM dsa_topics WHERE user_id = %s GROUP BY status", (user_id,))
    topics_status = cursor.fetchall()
    cursor.close()
    conn.close()
    return topics_status

def get_total_questions_solved(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT SUM(questions_solved) AS total_questions_solved FROM dsa_topics WHERE user_id = %s", (user_id,))
    questions = cursor.fetchone()
    cursor.close()
    conn.close()
    return questions

def get_topics_by_rank(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT topic_name, questions_solved FROM dsa_topics WHERE user_id = %s ORDER BY questions_solved DESC", (user_id,))
    ranked_topics = cursor.fetchall()
    cursor.close()
    conn.close()
    return ranked_topics

def get_company_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT SUM(CASE WHEN status='Applied' THEN 1 ELSE 0 END) AS 'applied', SUM(CASE WHEN status='OA' THEN 1 ELSE 0 END) AS 'oa', SUM(CASE WHEN status='Interview' THEN 1 ELSE 0 END) AS 'interview', SUM(CASE WHEN status='Selected' THEN 1 ELSE 0 END) AS 'selected', SUM(CASE WHEN status='Rejected' THEN 1 ELSE 0 END) AS 'rejected' FROM companies WHERE user_id = %s", (user_id,))
    company_status = cursor.fetchone()
    cursor.close()
    conn.close()
    return company_status

def get_notes_per_week(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT WEEK(created_at) AS week_number, COUNT(*) AS notes_count FROM notes WHERE user_id = %s GROUP BY WEEK(created_at)", (user_id,))
    weekly_notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return weekly_notes