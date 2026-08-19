from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import get_db_connection
from app.decorators import login_required

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
@login_required
def home():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM dsa_topics WHERE user_id = %s", (user_id,))
    total_topics = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS completed FROM dsa_topics WHERE user_id = %s AND status = 'Completed'", (user_id,))
    completed_topics = cursor.fetchone()['completed']

    cursor.execute("SELECT COUNT(*) AS total FROM companies WHERE user_id = %s", (user_id,))
    total_companies = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM notes WHERE user_id = %s", (user_id,))
    total_notes = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    return render_template('dashboard.html', total_topics=total_topics, completed_topics=completed_topics, total_companies=total_companies, total_notes=total_notes)

#DSA Tracker

@pages_bp.route('/dsa')
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

@pages_bp.route('/dsa/add', methods=['POST'])
@login_required
def add_dsa_topic():
    user_id = session['user_id']
    topic_name = request.form['topic_name']

    if not topic_name:
        flash('Topic name is required.')
        return redirect(url_for('pages.dsa_tracker'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dsa_topics (user_id, topic_name) VALUES (%s, %s)", (user_id, topic_name))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Topic added!')
    return redirect(url_for('pages.dsa_tracker'))

@pages_bp.route('/dsa/update/<int:topic_id>', methods=['POST'])
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
    return redirect(url_for('pages.dsa_tracker'))

@pages_bp.route('/dsa/delete/<int:topic_id>', methods=['POST'])
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
    return redirect(url_for('pages.dsa_tracker'))

#Company Tracker

@pages_bp.route('/companies')
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

@pages_bp.route('/companies/add', methods=['POST'])
@login_required
def add_company_name():
    user_id = session['user_id']
    company_name = request.form['company_name']
    status = request.form['status']

    if not company_name:
        flash('Company name is required.')
        return redirect(url_for('pages.company_tracker'))

    if len(company_name) > 100:
        flash('Company name must be 100 characters or fewer.')
        return redirect(url_for('pages.company_tracker'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO companies (user_id, company_name, status) VALUES (%s, %s, %s)", (user_id, company_name, status))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Company added!')
    return redirect(url_for('pages.company_tracker'))

@pages_bp.route('/companies/update/<int:company_id>', methods=['POST'])
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
    return redirect(url_for('pages.company_tracker'))

@pages_bp.route('/companies/delete/<int:company_id>', methods=['POST'])
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
    return redirect(url_for('pages.company_tracker'))

@pages_bp.route('/notes')
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

@pages_bp.route('/notes/add', methods=['POST'])
@login_required
def add_notes():
    user_id = session['user_id']
    title = request.form['title']
    content = request.form['content']

    if not title:
        flash('Title is required.')
        return redirect(url_for('pages.notes'))

    if len(title) > 150:
            flash('Title must be 150 characters or fewer.')
            return redirect(url_for('pages.notes'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)", (user_id, title, content))
    conn.commit()
    cursor.close()
    conn.close()

    flash('New note added!')
    return redirect(url_for('pages.notes'))

@pages_bp.route('/notes/edit/<int:note_id>')
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
        return redirect(url_for('pages.notes'))

    return render_template('edit_note.html', note=note)

@pages_bp.route('/notes/update/<int:note_id>', methods=['POST'])
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
    return redirect(url_for('pages.notes'))

@pages_bp.route('/notes/delete/<int:note_id>', methods=['POST'])
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
    return redirect(url_for('pages.notes'))

@pages_bp.route('/profile')
@login_required
def profile():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, full_name, email, bio, updated_at FROM users WHERE id = %s", (user_id,))
    profile = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('profile.html', profile=profile)

