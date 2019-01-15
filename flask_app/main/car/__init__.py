from flask import Blueprint
car = Blueprint('car', __name__, url_prefix='/car')
from . import views, errors