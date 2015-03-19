from flask import Blueprint

connect = Blueprint('connect', __name__)

from . import views
