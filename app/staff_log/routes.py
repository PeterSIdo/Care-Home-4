from flask import render_template, request, redirect, url_for, flash
from app.staff_log import bp
import sqlite3
from datetime import datetime
import uuid

@bp.route('/create_staff_log_tab', methods=['POST'])
def create_staff_log_tab():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff_log (
            id TEXT PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            entry_category TEXT,
            description TEXT,
            suggested_completion_time DATETIME,
            initiator TEXT,
            completer TEXT
        )
    ''')  
    conn.commit()
    conn.close()
    flash('Staff log table created successfully!', 'success')
    return redirect(url_for('staff_log.view_staff_log'))

@bp.route('/create_staff_log', methods=['GET', 'POST'])
def create_staff_log():
    if request.method == 'POST':
        entry_category = request.form['entry_category']
        description = request.form['description']
        suggested_completion_time = request.form['suggested_completion_time']      
        initiator = request.form['initiator']
        completer = request.form.get('completer', '')

        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO staff_log (id, timestamp, entry_category, description, suggested_completion_time, initiator, completer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(uuid.uuid4()), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), entry_category, description, suggested_completion_time, initiator, completer))
        conn.commit()
        conn.close()

        flash('New staff log entry created successfully!', 'success')
        return redirect(url_for('staff_log.view_staff_log'))

    return render_template('create_staff_log.html')

@bp.route('/view_staff_log', methods=['GET'])
def view_staff_log():
    # Get filter parameters from request arguments
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    task_completed = request.args.get('task_completed')  # 'all', 'completed', 'not_completed'

    # Connect to the database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()

    # Build the base query
    query = 'SELECT * FROM staff_log WHERE 1=1'
    params = []

    # Add date filtering
    if start_date and end_date:
        query += ' AND timestamp BETWEEN ? AND ?'
        params.extend([start_date, end_date])

    # Add task completion filtering
    if task_completed == 'completed':
        query += ' AND task_completed = 1'
    elif task_completed == 'not_completed':
        query += ' AND task_completed = 0'

    # Execute the query
    cursor.execute(query, params)
    logs = cursor.fetchall()
    conn.close()

    # Format the suggested_completion_time
    formatted_logs = []
    for log in logs:
        log = list(log)
        log[4] = datetime.strptime(log[4], '%Y-%m-%dT%H:%M').strftime('%d-%m-%Y %H:%M') 
        formatted_logs.append(log)

    return render_template('view_staff_log.html', logs=formatted_logs)


@bp.route('/submit_staff_log', methods=['POST'])
def submit_staff_log():
    # Extract data from the form
    entry_category = request.form['entry_category']
    description = request.form['description']
    suggested_completion_time = request.form['suggested_completion_time']
    initiator = request.form['initiator']
    completer = request.form.get('completer', '')

    # Generate a timestamp for the current date and time
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Database insertion logic
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO staff_log (timestamp, entry_category, description, suggested_completion_time, initiator, completer)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (current_timestamp, entry_category, description, suggested_completion_time, initiator, completer))
    conn.commit()
    conn.close()

    flash('New staff log entry created successfully!', 'success')
    return redirect(url_for('staff_log.view_staff_log'))

@bp.route('/update_staff_log/<log_id>', methods=['GET', 'POST'])
def update_staff_log(log_id):
    if request.method == 'POST':
        completer = request.form['completer']
        task_completed = request.form.get('task_completed', 'off') == 'on'

        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE staff_log
            SET completer = ?, task_completed = ?
            WHERE id = ?
        ''', (completer, task_completed, log_id))
        conn.commit()
        conn.close()

        flash('Staff log entry updated successfully!', 'success')
        return redirect(url_for('staff_log.view_staff_log'))

    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM staff_log WHERE id = ?', (log_id,))
    log = cursor.fetchone()
    conn.close()

    return render_template('update_staff_log.html', log=log)