from flask import render_template, session, redirect, url_for, flash, request
from app.main import bp
from app.login.forms import LoginForm  # Import the LoginForm
import sqlite3
from app.login_check import login_required

@bp.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        username = session.get('username', 'Guest')
        return render_template('index.html', username=username)
    else:
        form = LoginForm()  # Create an instance of LoginForm
        return render_template('login.html', form=form)  # Pass the form to the template

@bp.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login.login'))

@bp.route('/admin_panel')
@login_required(user_mode='a')  # Apply the login_required decorator
def admin_panel():
    return render_template('admin_panel.html')


# c:/Users/Peter/Documents/Care-Home-4/app/main/routes.py
@bp.route('/carer_menu')
@login_required(user_mode='c')
def carer_menu():
    return render_template('carer_menu.html')

@bp.route('/carer_input', methods=['GET', 'POST'])
def carer_input():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'c':
        if request.method == 'POST':
            unit_name = request.form.get('unit_name')
            resident_initials = request.form.get('resident_initials')
            first_name = request.form.get('first_name')
            service_name = request.form.get('service_name')
            
            if not unit_name or not resident_initials or not service_name:
                flash('Please enter unit name, resident initials, and select a service.')
                return redirect(url_for('main.carer_input'))
            
            # Redirect to data_collection blueprint with selected service
            return redirect(url_for('data_collection.collect_data', unit_name=unit_name, resident_initials=resident_initials, first_name=first_name, service_name=service_name))
        
        # Fetch service list and unit list from the database
        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, service_name FROM service_list')
        services = cursor.fetchall()
        cursor.execute('SELECT DISTINCT unit_name FROM units')  # Updated query
        units = cursor.fetchall()
        conn.close()
        
        return render_template('carer_input.html', services=services, units=units)
    return redirect(url_for('login.login'))

@bp.route('/get_residents', methods=['GET'])
def get_residents():
    unit_name = request.args.get('unit_name')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT resident_initials FROM residents WHERE unit_name = ?', (unit_name,))
    residents = cursor.fetchall()
    conn.close()
    return {'residents': [resident[0] for resident in residents]}



@bp.route('/enter_resident', methods=['GET', 'POST'])
def enter_resident():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            surname = request.form.get('surname')
            unit_name = request.form.get('unit_name')
            room_nr = request.form.get('room_nr')

            # Convert room_nr to an integer
            try:
                room_nr = int(room_nr)
            except ValueError:
                flash('Room number must be an integer.')
                return redirect(url_for('main.enter_resident'))
            
            # Calculate resident initials
            initials = first_name[0].upper() + surname[0].upper()
            resident_initials = f"{unit_name}{room_nr:02d}{initials}"

            # Connect to the database
            conn = sqlite3.connect('care4.db')
            cursor = conn.cursor()

            # Create table if it does not exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS residents (
                                id INTEGER PRIMARY KEY, 
                                first_name TEXT, 
                                surname TEXT, 
                                unit_name TEXT, 
                                room_nr INTEGER,
                                resident_initials TEXT)''')

            # Insert data into the table
            cursor.execute('INSERT INTO residents (first_name, surname, unit_name, room_nr, resident_initials) VALUES (?, ?, ?, ?, ?)', 
                           (first_name, surname, unit_name, room_nr, resident_initials))

            # Commit changes and close connection
            conn.commit()
            conn.close()

            flash('Resident added successfully!')
            return redirect(url_for('main.enter_resident'))

        return render_template('enter_resident.html')
    return redirect(url_for('login.login'))



# Code bellow this line is NOT in Use 

@bp.route('/enter_service_list', methods=['GET', 'POST'])
def enter_service_list():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for service list
            pass
        return render_template('enter_service_list.html')
    return redirect(url_for('login.login'))

@bp.route('/enter_fluid_list', methods=['GET', 'POST'])
def enter_fluid_list():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for fluid list
            pass
        return render_template('enter_fluid_list.html')
    return redirect(url_for('login.login'))

@bp.route('/enter_food_list', methods=['GET', 'POST'])
def enter_food_list():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for food list
            pass
        return render_template('enter_food_list.html')
    return redirect(url_for('login.login'))

@bp.route('/enter_care_list', methods=['GET', 'POST'])
def enter_care_list():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for care list
            pass
        return render_template('enter_care_list.html')
    return redirect(url_for('login.login'))

@bp.route('/enter_bowel_list', methods=['GET', 'POST'])
def enter_bowel_list():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for bowel list
            pass
        return render_template('enter_bowel_list.html')
    return redirect(url_for('login.login'))


@bp.route('/manage_database', methods=['GET', 'POST'])
def manage_database():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        unit_name = request.form.get('unit_name')
        room_nr = request.form.get('room_nr')

        # Connect to the database
        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()

        # Create table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS residents (
                            id INTEGER PRIMARY KEY, 
                            first_name TEXT, 
                            surname TEXT, 
                            unit_name TEXT, 
                            room_nr INTEGER)''')

        # Insert data into the table
        if first_name and surname:
            cursor.execute('INSERT INTO residents (first_name, surname, unit_name, room_nr) VALUES (?, ?, ?, ?)', 
                           (first_name, surname, unit_name, room_nr))

        # Commit changes and close connection
        conn.commit()
        conn.close()

        flash('Database updated successfully!')
        return redirect(url_for('main.manage_database'))

    return render_template('manage_database.html')