from flask import request
# from flask import current_app
from flask import render_template
from flask_app.main import main
from flask_script import Manager, Server
# from .forms import LoginForm, RegisterForm


@main.route('/')
def index():
    return render_template('index.html')
    # user_agent = request.headers.get('user-agent')
    # return '这是该网页的user agent：%s' % user_agent

