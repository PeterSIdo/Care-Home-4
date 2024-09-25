# VC:\Users\Peter\Documents\Care-Home-4\app\admin\routes.py
from flask import render_template, request, redirect, url_for, flash, session
from app.admin import bp  # Ensure this import is correct
import sqlite3
from datetime import datetime
from app.login_check import login_required
from app.utils import generate_unique_id  # Import the function from utils.py

@bp.route('/admin_dashboard')
@login_required(user_mode='a')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# c:/Users/Peter/Documents/Care-Home-4/app/admin/routes.py
@bp.route('/enter_resident', methods=['GET', 'POST'])
def enter_resident():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            resident_name = request.form.get('resident_name')
            resident_surname = request.form.get('resident_surname')
            unit_name = request.form.get('unit_name')
            room_nr = request.form.get('room_nr')
            action = request.form.get('action')

            # Convert room_nr to an integer
            try:
                room_nr = int(room_nr)
            except ValueError:
                flash('Room number must be an integer.')
                return redirect(url_for('admin.enter_resident'))

            # Connect to the database
            conn = sqlite3.connect('care4.db')
            cursor = conn.cursor()

            # Check if the unit name and room number already exist
            cursor.execute('SELECT * FROM residents WHERE unit_name = ? AND room_nr = ?', (unit_name, room_nr))
            existing_resident = cursor.fetchone()

            if existing_resident and action != 'overwrite':
                # If resident exists and action is not overwrite, ask for confirmation
                conn.close()
                return render_template('enter_resident.html', resident_name=resident_name, resident_surname=resident_surname, unit_name=unit_name, room_nr=room_nr, confirm=True)

            if action == 'cancel':
                # If action is cancel, redirect to the form without changes
                conn.close()
                return redirect(url_for('admin.enter_resident'))

            # Calculate resident initials
            initials = resident_name[0].upper() + resident_surname[0].upper()
            resident_initials = f"{unit_name}{room_nr:02d}{initials}"

            # Generate unique ID
            resident_unique_id = generate_unique_id(resident_name, resident_surname)

            if existing_resident:
                # If overwriting, update the existing record
                cursor.execute('''
                    UPDATE residents
                    SET resident_name = ?, resident_surname = ?, resident_initials = ?, resident_unique_id = ?
                    WHERE unit_name = ? AND room_nr = ?
                ''', (resident_name, resident_surname, resident_initials, resident_unique_id, unit_name, room_nr))
            else:
                # Insert new resident data into the database
                cursor.execute('''
                    INSERT INTO residents (resident_unique_id, resident_name, resident_surname, unit_name, room_nr, resident_initials)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (resident_unique_id, resident_name, resident_surname, unit_name, room_nr, resident_initials))
                
            # Insert data into resident_identifiers table
            cursor.execute('''
                INSERT INTO resident_identifiers (resident_unique_id, resident_name, resident_surname)
                VALUES (?, ?, ?)
            ''', (resident_unique_id, resident_name, resident_surname))

            conn.commit()
            conn.close()

            flash('Resident added successfully.', 'success')
            return redirect(url_for('admin.enter_resident'))
    return render_template('enter_resident.html')


@bp.route('/list_all_residents')
@login_required(user_mode='a')
def list_all_residents():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT resident_initials, resident_name, resident_surname, unit_name, room_nr FROM residents')
    residents = cursor.fetchall()
    conn.close()
    return render_template('list_all_residents.html', residents=residents)

@bp.route('/residents_observations_input', methods=['GET', 'POST'])
def residents_observations_input():
    if request.method == 'POST':
        # Collect form data
        resident_initials = request.form.get('resident_initials')
        unit_name = request.form.get('unit_name')
        observation_name = request.form.get('observation_name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        observation_reason = request.form.get('observation_reason')
        observation_notes = request.form.get('observation_notes')   
        staff_initials = request.form.get('staff_initials')
        
        # Validate form data
        if not (resident_initials and unit_name):
            flash('Please fill out all required fields.')
            return redirect(url_for('staff_board.residents_observations_input'))

        # Insert data into the database
        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO residents_observations_chart (
                resident_initials, unit_name, observation_name, start_date, end_date, observation_reason, observation_notes, staff_initials
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (resident_initials, unit_name, observation_name, start_date, end_date, observation_reason, observation_notes, staff_initials))
        conn.commit()
        conn.close()

        flash('Observation recorded successfully!', 'success')
        return redirect(url_for('admin.residents_observations_input'))

    # Fetch unit names from the database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT unit_name FROM units')
    units = cursor.fetchall()
    
    cursor.execute('SELECT DISTINCT observation_name FROM residents_observations_list')
    observations = cursor.fetchall()
    conn.close()

    return render_template('residents_observations_input.html', units=units, observations=observations)

# Filter and re-submit residents by Unit name and Room number
@bp.route('/filter_and_resubmit_residents', methods=['GET'])
def filter_and_resubmit_residents():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    
    # Read all rows from the residents table
    cursor.execute('SELECT resident_name, resident_surname, unit_name, room_nr, resident_initials FROM residents')
    residents = cursor.fetchall()
    
    # Sort the table by Unit name and Room nr
    residents_sorted = sorted(residents, key=lambda x: (x[2], x[3]))
    
    # Clear the table
    cursor.execute('DELETE FROM residents')
    
        
    # Reset the id sequence
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="residents"')
    
    # Re-insert the sorted data without the id column
    for resident in residents_sorted:
        cursor.execute('INSERT INTO residents (resident_name, resident_surname, unit_name, room_nr, resident_initials) VALUES (?, ?, ?, ?, ?)', resident)
        
    # Commit changes and close session
    conn.commit()
    conn.close()
    
    flash('Residents have been filtered and re-submitted successfully!', 'success')
    return redirect(url_for('admin.list_all_residents'))