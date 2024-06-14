# app/__init__.py
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    Bootstrap(app)  # Initialize Bootstrap-Flask

    @app.route('/')
    def index():
        return render_template('index.html')

    return app