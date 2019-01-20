from flask import request
# from flask import current_app
from flask import render_template
from . import car
from flask_script import Manager, Server
# from .forms import LoginForm, RegisterForm


@car.route('/')
def index():
    return render_template('index.html')


@car.route('/proinfo/')
def proinfo():
    return render_template('car/proinfo.html')


@car.route('/recommend/')
def recommend():
    return render_template('car/recommend.html')


@car.route('/select/')
def select():
    return render_template('car/select.html')


@car.route('/service/')
def service():
    return render_template('car/service.html')


@car.route('/business/')
def business():
    return render_template('car/business.html')


@car.route('/job/')
def job():
    return render_template('car/job.html')


@car.route('/contact/')
def contact():
    return render_template('car/contact.html')


