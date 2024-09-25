# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py
from flask import render_template, request, redirect, url_for, flash, session
from app.data_collection import bp
import sqlite3
from datetime import datetime
from app.login_check import login_required

import speech_recognition as sr
# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py

@bp.route('/process_audio', methods=['POST'])
def process_audio():
    audio_file = request.files['audio']
    # Assuming voice_to_text.py has a function `transcribe_audio` to process the audio file
    from SpeechRecog.voice_to_text import transcribe_audio
    recognized_text = transcribe_audio(audio_file)
    return jsonify({'recognized_text': recognized_text})



@bp.route('/collect_data')
@login_required()
def collect_data():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    resident_name = request.args.get('resident_name')
    service_name = request.args.get('service_name')
    return render_template('collect_data.html', unit_name=unit_name, resident_initials=resident_initials, resident_name=resident_name, service_name=service_name)

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
    cursor.execute('SELECT resident_initials, resident_name FROM residents WHERE unit_name = ?', (unit_name,))
    residents = cursor.fetchall()
    conn.close()
    return render_template('select_resident.html', residents=residents, unit_name=unit_name)

# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py

@bp.route('/data_collection_logic', methods=['POST'])
def data_collection_logic():
    unit_name = request.form.get('unit_name')
    resident_initials = request.form.get('resident_initials')
    service_name = request.form.get('service_name')
    resident_name= request.form.get('resident_name')
    if service_name == 'fluid intake':
        return redirect(url_for('data_collection.fluid_intake', unit_name=unit_name, resident_initials=resident_initials))
    elif service_name == 'food intake':
        return redirect(url_for('data_collection.food_intake', unit_name=unit_name, resident_initials=resident_initials))
    elif service_name == 'personal care':
        return redirect(url_for('data_collection.personal_care_input', unit_name=unit_name, resident_initials=resident_initials))
    elif service_name == 'cardex':
        return redirect(url_for('data_collection.cardex', unit_name=unit_name, resident_initials=resident_initials))
    elif service_name == 'care frequency':
        return redirect(url_for('data_collection.care_frequency', unit_name=unit_name, resident_initials=resident_initials))
    elif service_name == 'bowels observation':
        return redirect(url_for('data_collection.bowel_observation', unit_name=unit_name, resident_initials=resident_initials))    
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
    staff_initials = request.form.get('staff_initials').upper()  # Retrieve staff_initials from the form data
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
    food_name = request.form.get('food_name')  # Updated variable name
    food_volume = request.form.get('food_volume')
    food_note = request.form.get('food_note')
    input_time = request.form.get('input_time')  # Retrieve input_time from the form data
    staff_initials = request.form.get('staff_initials').upper()  # Convert to uppercase
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
            food_name TEXT,
            food_volume INTEGER,
            food_note TEXT,
            staff_initials TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO food_chart (resident_initials, timestamp, food_name, food_amount, food_note, staff_initials)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (resident_initials, timestamp, food_name, food_volume, food_note, staff_initials))
    conn.commit()
    conn.close()

    flash('Food intake recorded successfully!', 'success')
    return redirect(url_for('data_collection.food_intake', unit_name=request.form.get('unit_name'), resident_initials=resident_initials))

# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py
    # Personal care input
@bp.route('/personal_care_input')
def personal_care_input():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, personal_care_name FROM personal_care_list')
    personal_care_list = cursor.fetchall()
    conn.close()
    return render_template('personal_care_form.html', personal_care_list= personal_care_list, unit_name=unit_name, resident_initials=resident_initials)

@bp.route('/submit_personal_care', methods=['POST'])
def submit_personal_care():
    unit_name = request.form.get('unit_name')
    resident_initials = request.form.get('resident_initials')
    personal_care_type = request.form.get('personal_care_type')
    personal_care_note = request.form.get('personal_care_note')
    personal_care_duration = request.form.get('personal_care_duration')
    input_time = request.form.get('input_time')
    staff_initials = request.form.get('staff_initials').upper()
    timestamp = datetime.now().strftime('%Y-%m-%d') + ' ' + input_time + ':00'

    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()

    # Validation snippet to check if staff_initials exist in the staff table
    cursor.execute('SELECT 1 FROM staff WHERE staff_initials = ?', (staff_initials,))
    if cursor.fetchone() is None:
        conn.close()
        flash('Invalid staff initials. Please check and try again.', 'amber')
        return redirect(url_for('data_collection.personal_care_input', unit_name=unit_name, resident_initials=resident_initials))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal_care_chart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident_initials TEXT,
            timestamp TEXT,
            personal_care_type TEXT,
            personal_care_duration INTEGER,
            personal_care_note TEXT,
            staff_initials TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO personal_care_chart (resident_initials, timestamp, personal_care_type, personal_care_note, personal_care_duration, staff_initials)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (resident_initials, timestamp, personal_care_type, personal_care_note, personal_care_duration,staff_initials))
    conn.commit()
    conn.close()

    flash('Personal care entry recorded successfully!', 'success')
    return redirect(url_for('data_collection.personal_care_input', unit_name=unit_name, resident_initials=resident_initials))


@bp.route('/cardex')
def cardex():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, cardex_text FROM cardex_chart')
    cardex_text = cursor.fetchall()
    conn.close()
    return render_template('cardex_form.html', cardex_text=cardex_text, unit_name=unit_name, resident_initials=resident_initials)

@bp.route('/submit_cardex', methods=['POST'])
def submit_cardex():
    resident_initials = request.form.get('resident_initials')
    cardex_text = request.form.get('cardex_text')
    input_time = request.form.get('input_time')  # Retrieve input_time from the form data
    staff_initials = request.form.get('staff_initials').upper()  # Retrieve staff_initials from the form data
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
        CREATE TABLE IF NOT EXISTS cardex_chart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident_initials TEXT,
            timestamp TEXT,
            cardex_text TEXT,
            staff_initials TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO cardex_chart (resident_initials, timestamp, cardex_text, staff_initials)
        VALUES (?, ?, ?, ?)
    ''', (resident_initials, timestamp, cardex_text, staff_initials))
    conn.commit()
    conn.close()

    flash('Cardex entry recorded successfully!', 'success')
    return redirect(url_for('data_collection.cardex', unit_name=request.form.get('unit_name'), resident_initials=resident_initials))

# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py
# Care frequency route
@bp.route('/care_frequency')
@login_required()
def care_frequency():
    resident_initials = request.args.get('resident_initials')
    return render_template('care_frequency_form.html', resident_initials=resident_initials)

@bp.route('/submit_care_frequency', methods=['POST'])
@login_required()
def submit_care_frequency():
    # Collect form data
    resident_initials = request.form.get('resident_initials')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mattress_appropriate = request.form.get('mattress_appropriate')
    cushion_appropriate = request.form.get('cushion_appropriate')
    functionality_check = request.form.get('functionality_check')
    pressure_areas_checked = request.form.get('pressure_areas_checked')
    redness_present = request.form.get('redness_present')
    position = request.form.get('position')
    incontinence_urine = request.form.get('incontinence_urine')
    incontinence_bowels = request.form.get('incontinence_bowels')
    diet_intake = request.form.get('diet_intake')
    fluid_intake = request.form.get('fluid_intake')
    supplement_intake = request.form.get('supplement_intake')
    staff_initials = request.form.get('staff_initials').upper()
    notes = request.form.get('notes')

    # Insert data into the database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO care_frequency_chart (
            resident_initials, timestamp, mattress_appropriate, cushion_appropriate,
            functionality_check, pressure_areas_checked, redness_present, position,
            incontinence_urine, incontinence_bowels, diet_intake, fluid_intake,
            supplement_intake, staff_initials, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        resident_initials, timestamp, mattress_appropriate, cushion_appropriate,
        functionality_check, pressure_areas_checked, redness_present, position,
        incontinence_urine, incontinence_bowels, diet_intake, fluid_intake,
        supplement_intake, staff_initials, notes
    ))
    conn.commit()
    conn.close()

    flash('Care frequency data submitted successfully!', 'success')
    return redirect(url_for('main.carer_menu'))

@bp.route('/bowel_observation')
def bowel_observation():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, bowel_name, bowel_size, bowel_mode FROM bowel_list')
    bowel_list = cursor.fetchall()
    conn.close()
    return render_template('bowel_observation_form.html', bowel_list=bowel_list, unit_name=unit_name, resident_initials=resident_initials)

@bp.route('/submit_bowel_observation', methods=['POST'])
def submit_bowel_observation():
    resident_initials = request.form.get('resident_initials')
    bowel_type = request.form.get('bowel_type')
    bowel_size = request.form.get('bowel_size')
    bowel_mode = request.form.get('bowel_mode')
    bowel_note = request.form.get('bowel_note')
    input_time = request.form.get('input_time')
    staff_initials = request.form.get('staff_initials').upper()
    timestamp = datetime.now().strftime('%Y-%m-%d') + ' ' + input_time + ':00'

    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM staff WHERE staff_initials = ?', (staff_initials,))
    if cursor.fetchone() is None:
        conn.close()
        flash('Invalid staff initials. Please check and try again.', 'amber')
        return redirect(url_for('data_collection.bowel_observation', unit_name=request.form.get('unit_name'), resident_initials=resident_initials))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bowel_chart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident_initials TEXT,
            timestamp TEXT,
            bowel_type TEXT,
            bowel_size TEXT,
            bowel_mode TEXT,
            bowel_note TEXT,
            staff_initials TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO bowel_chart (resident_initials, timestamp, bowel_type, bowel_size, bowel_mode, bowel_note, staff_initials)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (resident_initials, timestamp, bowel_type, bowel_size, bowel_mode, bowel_note, staff_initials))
    conn.commit()
    conn.close()

    flash('Bowel observation recorded successfully!', 'success')
    return redirect(url_for('main.carer_input'))