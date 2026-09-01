from app.extensions import get_db_connection

def get_goals_for_user(user_id, week_start_date):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM goals WHERE user_id = %s AND week_start_date = %s", (user_id, week_start_date))
    goals = cursor.fetchall()
    cursor.close()
    conn.close()
    return goals

def create_goal(user_id, description, target_count, week_start_date):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO goals (user_id, description, target_count, week_start_date) VALUES (%s, %s, %s, %s)", (user_id, description, target_count, week_start_date))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM goals WHERE id = %s", (new_id,))
    new_goal = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_goal

def update_goal_progress(goal_id, user_id, current_count):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE goals SET current_count = %s WHERE id = %s AND user_id = %s", (current_count, goal_id, user_id))
    conn.commit()
    cursor.execute("SELECT * FROM goals WHERE id = %s AND user_id = %s", (goal_id, user_id))
    updated_goal = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_goal

def delete_goal(goal_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM goals WHERE id = %s AND user_id = %s", (goal_id, user_id))
    conn.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return deleted