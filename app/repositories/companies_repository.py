from app.extensions import get_db_connection

def get_companies_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies WHERE user_id = %s", (user_id,))
    companies = cursor.fetchall()
    cursor.close()
    conn.close()
    return companies

def insert_company(user_id, company_name, status):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO companies (user_id, company_name, status) VALUES (%s, %s, %s)", (user_id, company_name, status))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM companies WHERE id = %s", (new_id,))
    new_company = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_company

def update_company(company_id, user_id, status):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE companies SET status = %s WHERE id = %s AND user_id = %s", (status, company_id, user_id))
    conn.commit()
    cursor.execute("SELECT * FROM companies WHERE id = %s AND user_id = %s", (company_id, user_id))
    updated_company = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_company

def delete_company(company_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM companies WHERE id = %s AND user_id = %s", (company_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()