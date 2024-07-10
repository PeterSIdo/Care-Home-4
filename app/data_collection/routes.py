# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py
from flask import render_template, request, redirect, url_for, flash, session
from app.data_collection import bp
import sqlite3
from datetime import datetime
from app.login_check import login_required

@bp.route('/collect_data')
@login_required()
def collect_data():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    first_name = request.args.get('first_name')
    service_name = request.args.get('service_name')
    return render_template('collect_data.html', unit_name=unit_name, resident_initials=resident_initials, first_name=first_name, service_name=service_name)

@bp.route('/select_unit')
def select_unit():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT unit_name FROM units')
    units = cursor.fetchall()
    conn.close()
    return render_template('select_unit.html', units=units)


@bp.route('/select_resident', methods=['POST'])
def select_resident():
    unit_name = request.form.get('unit_name')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT resident_initials, first_name FROM residents WHERE unit_name = ?', (unit_name,))
    residents = cursor.fetchall()
    conn.close()
    return render_template('select_resident.html', residents=residents, unit_name=unit_name)

# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py

@bp.route('/data_collection_logic', methods=['POST'])
def data_collection_logic():
    unit_name = request.form.get('unit_name')
    resident_initials = request.form.get('resident_initials')
    service_name = request.form.get('service_name')
    first_name= request.form.get('first_name')
    if service_name == 'fluid intake':
        return redirect(url_for('data_collection.fluid_intake', unit_name=unit_name, resident_initials=resident_initials))
    elif service_name == 'food intake':
        return redirect(url_for('data_collection.food_intake', unit_name=unit_name, resident_initials=resident_initials))
    elif service_name == 'cardex':
        return redirect(url_for('data_collection.cardex', unit_name=unit_name, resident_initials=resident_initials))
    else:
        return redirect(url_for('data_collection.collect_data'))

@bp.route('/fluid_intake')
def fluid_intake():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, fluid_name FROM fluid_list')
    fluid_list = cursor.fetchall()
    conn.close()
    return render_template('fluid_intake_form.html', fluid_list=fluid_list, unit_name=unit_name, resident_initials=resident_initials)

# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py

@bp.route('/submit_fluid_intake', methods=['POST'])
def submit_fluid_intake():
    resident_initials = request.form.get('resident_initials')
    fluid_type = request.form.get('fluid_type')
    fluid_volume = request.form.get('fluid_volume')
    fluid_note = request.form.get('fluid_note')
    input_time = request.form.get('input_time')  # Retrieve input_time from the form data
    staff_initials = request.form.get('staff_initials')  # Retrieve staff_initials from the form data
    timestamp = datetime.now().strftime('%Y-%m-%d') + ' ' + input_time + ':00'

    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()

    # Validation snippet to check if staff_initials exist in the staff table
    cursor.execute('SELECT 1 FROM staff WHERE staff_initials = ?', (staff_initials,))
    if cursor.fetchone() is None:
        conn.close()
        flash('Invalid staff initials. Please check and try again.', 'amber')
        return redirect(url_for('data_collection.fluid_intake', unit_name=request.form.get('unit_name'), resident_initials=resident_initials))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fluid_chart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident_initials TEXT,
            timestamp TEXT,
            fluid_type TEXT,
            fluid_volume INTEGER,
            fluid_note TEXT,
            staff_initials TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO fluid_chart (resident_initials, timestamp, fluid_type, fluid_volume, fluid_note, staff_initials)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (resident_initials, timestamp, fluid_type, fluid_volume, fluid_note, staff_initials))
    conn.commit()
    conn.close()

    flash('The database was updated successfully!', 'success')
    return redirect(url_for('main.carer_input'))

@bp.route('/food_intake')
def food_intake():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, food_name FROM food_list')
    food_list = cursor.fetchall()
    conn.close()
    return render_template('food_intake_form.html', food_list=food_list, unit_name=unit_name, resident_initials=resident_initials)

# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py

@bp.route('/submit_food_intake', methods=['POST'])
def submit_food_intake():
    resident_initials = request.form.get('resident_initials')
    food_type = request.form.get('food_type')
    food_volume = request.form.get('food_volume')
    food_note = request.form.get('food_note')
    input_time = request.form.get('input_time')
    staff_initials = request.form.get('staff_initials')
    timestamp = datetime.now().strftime('%Y-%m-%d') + ' ' + input_time + ':00'

    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()

    # Validation snippet to check if staff_initials exist in the staff table
    cursor.execute('SELECT 1 FROM staff WHERE staff_initials = ?', (staff_initials,))
    if cursor.fetchone() is None:
        conn.close()
        flash('Invalid staff initials. Please check and try again.', 'amber')
        return redirect(url_for('data_collection.food_intake', unit_name=request.form.get('unit_name'), resident_initials=resident_initials))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_chart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident_initials TEXT,
            timestamp TEXT,
            food_type TEXT,
            food_volume INTEGER,
            food_note TEXT,
            staff_initials TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO food_chart (resident_initials, timestamp, food_type, food_amount, food_note, staff_initials)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (resident_initials, timestamp, food_type, food_volume, food_note, staff_initials))
    conn.commit()
    conn.close()

    flash('Food intake recorded successfully!', 'success')
    return redirect(url_for('data_collection.food_intake', unit_name=request.form.get('unit_name'), resident_initials=resident_initials))

@bp.route('/cardex')
def cardex():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, cardex_text FROM cardex')
    cardex_text = cursor.fetchall()
    conn.close()
    return render_template('cardex_form.html', cardex_text=cardex_text, unit_name=unit_name, resident_initials=resident_initials)

@bp.route('/submit_cardex', methods=['POST'])
def submit_cardex():
    resident_initials = request.form.get('resident_initials')
    cardex_text = request.form.get('cardex_text')
    input_time = request.form.get('input_time')  # Retrieve input_time from the form data
    staff_initials = request.form.get('staff_initials')  # Retrieve staff_initials from the form data
    timestamp = datetime.now().strftime('%Y-%m-%d') + ' ' + input_time + ':00'

    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()

    # Validation snippet to check if staff_initials exist in the staff table
    cursor.execute('SELECT 1 FROM staff WHERE staff_initials = ?', (staff_initials,))
    if cursor.fetchone() is None:
        conn.close()
        flash('Invalid staff initials. Please check and try again.', 'amber')
        return redirect(url_for('data_collection.cardex', unit_name=request.form.get('unit_name'), resident_initials=resident_initials))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cardex (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident_initials TEXT,
            timestamp TEXT,
            cardex_text TEXT,
            staff_initials TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO cardex (resident_initials, timestamp, cardex_text, staff_initials)
        VALUES (?, ?, ?, ?)
    ''', (resident_initials, timestamp, cardex_text, staff_initials))
    conn.commit()
    conn.close()

    flash('Cardex entry recorded successfully!', 'success')
    return redirect(url_for('data_collection.cardex', unit_name=request.form.get('unit_name'), resident_initials=resident_initials))