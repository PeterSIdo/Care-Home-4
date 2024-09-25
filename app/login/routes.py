#C:\Users\Peter\Documents\Care-Home-4\login\routes.py
#login\routes.py
from flask import render_template, redirect, url_for, flash, session
from app.login import bp
from app.login.forms import LoginForm
from app.login.login_evaluate import evaluate_login

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_mode = evaluate_login(username, password)
        if user_mode:
            session['user_mode'] = user_mode
            session['logged_in'] = True
            session['username'] = username
            if user_mode == 'a': 
                return redirect(url_for('admin.admin_dashboard'))
            if user_mode == 'c':
                return redirect(url_for('main.carer_menu'))
            # Add flash message if user_mode is not 'a' or 'c'
            flash('Access restricted to Admin and Carer only.')
        else:
            flash('Invalid username or password', 'success')
    return render_template('login.html', form=form)