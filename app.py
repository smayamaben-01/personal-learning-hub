from flask import Flask, render_template
from db import get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/dsa')
def dsa_tracker():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dsa_topics WHERE user_id = %s", (1,))
    topics = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dsa_tracker.html', topics=topics)