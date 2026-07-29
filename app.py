from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import config
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route('/')
@login_required
def home():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('register'))

        if len(username) > 50:
            flash('Username must be 50 characters or fewer.')
            return redirect(url_for('register'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('That username is already taken.')
            cursor.close()
            conn.close()
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

#DSA Tracker

@app.route('/dsa')
@login_required
def dsa_tracker():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dsa_topics WHERE user_id = %s", (user_id,))
    topics = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dsa_tracker.html', topics=topics)

@app.route('/dsa/add', methods=['POST'])
@login_required
def add_dsa_topic():
    user_id = session['user_id']
    topic_name = request.form['topic_name']

    if not topic_name:
        flash('Topic name is required.')
        return redirect(url_for('dsa_tracker'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dsa_topics (user_id, topic_name) VALUES (%s, %s)", (user_id, topic_name))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Topic added!')
    return redirect(url_for('dsa_tracker'))

@app.route('/dsa/update/<int:topic_id>', methods=['POST'])
@login_required
def update_dsa_topic(topic_id):
    user_id = session['user_id']
    status = request.form['status']
    questions_solved = request.form['questions_solved']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE dsa_topics SET status = %s, questions_solved = %s WHERE id = %s AND user_id = %s", (status, questions_solved, topic_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Topic updated!')
    return redirect(url_for('dsa_tracker'))

@app.route('/dsa/delete/<int:topic_id>', methods=['POST'])
@login_required
def delete_dsa_topic(topic_id):
    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dsa_topics WHERE id = %s AND user_id = %s", (topic_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Topic deleted.')
    return redirect(url_for('dsa_tracker'))

#Company Tracker

@app.route('/companies')
@login_required
def company_tracker():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies WHERE user_id = %s", (user_id,))
    names = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('company_tracker.html', companies=names)

@app.route('/companies/add', methods=['POST'])
@login_required
def add_company_name():
    user_id = session['user_id']
    company_name = request.form['company_name']
    status = request.form['status']

    if not company_name:
        flash('Company name is required.')
        return redirect(url_for('company_tracker'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO companies (user_id, company_name, status) VALUES (%s, %s, %s)", (user_id, company_name, status))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Company added!')
    return redirect(url_for('company_tracker'))

@app.route('/companies/update/<int:company_id>', methods=['POST'])
@login_required
def update_company_status(company_id):
    user_id = session['user_id']
    status = request.form['status']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE companies SET status = %s WHERE id = %s AND user_id = %s", (status, company_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Company status updated!')
    return redirect(url_for('company_tracker'))

@app.route('/companies/delete/<int:company_id>', methods=['POST'])
@login_required
def delete_company(company_id):
    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM companies WHERE id = %s AND user_id = %s", (company_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Company deleted.')
    return redirect(url_for('company_tracker'))

@app.route('/notes')
@login_required
def notes():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    all_notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('notes.html', notes=all_notes)

@app.route('/notes/add', methods=['POST'])
@login_required
def add_notes():
    user_id = session['user_id']
    title = request.form['title']
    content = request.form['content']

    if not title:
        flash('Title is required.')
        return redirect(url_for('notes'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)", (user_id, title, content))
    conn.commit()
    cursor.close()
    conn.close()

    flash('New note added!')
    return redirect(url_for('notes'))

@app.route('/notes/edit/<int:note_id>')
@login_required
def edit_note(note_id):
    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE id = %s AND user_id = %s", (note_id, user_id))
    note = cursor.fetchone()
    cursor.close()
    conn.close()

    if not note:
        flash('Note not found.')
        return redirect(url_for('notes'))

    return render_template('edit_note.html', note=note)

@app.route('/notes/update/<int:note_id>', methods=['POST'])
@login_required
def update_existing_note(note_id):
    user_id = session['user_id']
    title = request.form['title']
    content = request.form['content']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s AND user_id = %s ", (title, content, note_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Note updated!')
    return redirect(url_for('notes'))

@app.route('/notes/delete/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = %s AND user_id = %s", (note_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Note deleted.')
    return redirect(url_for('notes'))