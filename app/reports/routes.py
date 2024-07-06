# c:/Users/Peter/Documents/Care-Home-4/app/reports/routes.py
from flask import render_template, request, url_for, redirect, session, flash
from app.reports import bp
import sqlite3
from datetime import datetime

@bp.route('/report_selection', methods=['GET', 'POST'])
def report_selection():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'c':
        if request.method == 'POST':
            unit_name = request.form.get('unit_name')
            resident_initials = request.form.get('resident_initials')
            service_name = request.form.get('service_name')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            
            if not unit_name or not resident_initials or not service_name or not start_date or not end_date:
                flash('Please enter all required fields.')
                return redirect(url_for('reports.report_selection'))
            
            # Redirect to report_selection_logic blueprint with selected service and date range
            return redirect(url_for('reports.report_selection_logic', unit_name=unit_name, resident_initials=resident_initials, service_name=service_name, start_date=start_date, end_date=end_date))
        
        # Fetch service list and unit list from the database
        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, service_name FROM service_list')
        services = cursor.fetchall()
        cursor.execute('SELECT DISTINCT unit_name FROM units')  # Updated query
        units = cursor.fetchall()
        conn.close()
        
        return render_template('report_selection.html', services=services, units=units)
    return redirect(url_for('login.login'))

@bp.route('/report_selection_logic', methods=['GET', 'POST'])
def report_selection_logic():
    if request.method == 'POST':
        unit_name = request.form.get('unit_name')
        resident_initials = request.form.get('resident_initials')
        service_name = request.form.get('service_name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
    else:  # Handle GET request
        unit_name = request.args.get('unit_name')
        resident_initials = request.args.get('resident_initials')
        service_name = request.args.get('service_name')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

    if service_name == 'fluid intake':
        return redirect(url_for('reports.report_fluid', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    elif service_name == 'food intake':
        return redirect(url_for('data_collection.food_intake', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    else:
        return redirect(url_for('login.login'))

@bp.route('/report_fluid')
def report_fluid():
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM fluid_chart 
        WHERE resident_initials = ? AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()

    # Convert timestamp strings to datetime objects
    formatted_data = []
    for row in data:
        row = list(row)
        row[2] = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')  # Format without seconds
        formatted_data.append(row)

    return render_template('report_fluid.html', data=formatted_data)