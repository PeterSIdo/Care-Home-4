# c:/Users/Peter/Documents/Care-Home-4/app/staff_board/routes.py
from flask import render_template, request, redirect, url_for, flash
from app.staff_board import bp
import sqlite3
from datetime import datetime

@bp.route('/staff_dashboard')
def staff_dashboard():
    return render_template('staff_dashboard.html')



# c:/Users/Peter/Documents/Care-Home-4/app/staff_board/routes.py
@bp.route('/residents_observations_chart')
def residents_observations_chart():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    
    # Fetch only non-expired records
    cursor.execute('''
        SELECT * FROM residents_observations_chart
        WHERE end_date > ?
    ''', (datetime.now().strftime('%Y-%m-%dT%H:%M'),))
    
    observations = cursor.fetchall()
    conn.close()

    # Format the start_date and end_date
    formatted_observations = []
    for observation in observations:
        observation = list(observation)
        observation[4] = datetime.strptime(observation[4], '%Y-%m-%dT%H:%M').strftime('%d-%m-%y %H:%M')
        observation[5] = datetime.strptime(observation[5], '%Y-%m-%dT%H:%M').strftime('%d-%m-%y %H:%M')
        formatted_observations.append(observation)

    return render_template('residents_observations_chart.html', observations=formatted_observations)