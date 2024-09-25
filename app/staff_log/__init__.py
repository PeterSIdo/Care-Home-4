from flask import Blueprint

bp = Blueprint('staff_log', __name__)

from app.staff_log import routes