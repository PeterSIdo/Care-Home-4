# c:/Users/Peter/Documents/Care-Home-4/app/staff_board/__init__.py
from flask import Blueprint

bp = Blueprint('staff_board', __name__)

from app.staff_board import routes