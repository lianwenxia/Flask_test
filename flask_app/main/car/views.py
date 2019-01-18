from flask import request
# from flask import current_app
from flask import render_template
from . import car
from flask_script import Manager, Server
# from .forms import LoginForm, RegisterForm


@car.route('/')
def index():
    return render_template('index.html')


