# c:/Users/Peter/Documents/Care-Home-4/app/__init__.py
from flask import Flask, session,render_template
from config import Config
from datetime import datetime
from flask_bootstrap import Bootstrap5

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    Bootstrap5(app)  # Initialize Flask-Bootstrap
        
    @app.before_request
    def set_current_time():
        session['current_time'] = datetime.now()

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.login import bp as login_bp
    app.register_blueprint(login_bp)

    from app.data_collection import bp as data_collection_bp
    app.register_blueprint(data_collection_bp)

    from app.charts import bp as charts_bp
    app.register_blueprint(charts_bp)
    
    from app.reports import bp as reports_bp
    app.register_blueprint(reports_bp)
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    from app.staff_board import bp as staff_board_bp
    app.register_blueprint(staff_board_bp, url_prefix='/staff_board')

    return app