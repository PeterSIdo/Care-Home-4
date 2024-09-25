from flask import render_template, session, redirect, url_for, flash, request
from app.main import bp
from app.login.forms import LoginForm  # Import the LoginForm
import sqlite3
from app.login_check import login_required

@bp.route('/about_care_home')
def about_care_home():
    return render_template('about_care_home.html')

@bp.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

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
            
            service_name = request.form.get('service_name')
            
            if not unit_name or not resident_initials or not service_name:
                flash('Please enter unit name, resident initials, and select a service.')
                return redirect(url_for('main.carer_input'))
            
            # Redirect to data_collection blueprint with selected service
            return redirect(url_for('data_collection.collect_data', unit_name=unit_name, resident_initials=resident_initials, service_name=service_name))
        
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
        resident_name = request.form.get('resident_name')
        resident_surname = request.form.get('resident_surname')
        unit_name = request.form.get('unit_name')
        room_nr = request.form.get('room_nr')

        # Connect to the database
        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()

        # Create table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS residents (
                            id INTEGER PRIMARY KEY, 
                            resident_name TEXT, 
                            resident_surname TEXT, 
                            unit_name TEXT, 
                            room_nr INTEGER)''')

        # Insert data into the table
        if resident_name and resident_surname:
            cursor.execute('INSERT INTO residents (resident_name, resident_surname, unit_name, room_nr) VALUES (?, ?, ?, ?)', 
                           (resident_name, resident_surname, unit_name, room_nr))

        # Commit changes and close connection
        conn.commit()
        conn.close()

        flash('Database updated successfully!')
        return redirect(url_for('main.manage_database'))

    return render_template('manage_database.html')