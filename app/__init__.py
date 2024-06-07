# c:/Users/Peter/Documents/Care-Home-4/app/__init__.py
from flask import Flask, session
from config import Config
from datetime import datetime

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
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

    from app.dashboards import bp as dashboards_bp
    app.register_blueprint(dashboards_bp)

    return app