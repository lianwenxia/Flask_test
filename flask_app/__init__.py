from flask import Flask, url_for
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager, current_user
from flask_admin import Admin, BaseView, expose, form

import os.path as op

file_path = op.join(op.dirname(__file__), 'static')

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'users.login'

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
admin = Admin(name=u'鑫与汇后台', template_mode='bootstrap2')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)
    # 附加路由和自定义的错误页面
    from flask_app.main import main as main_blueprint
    from flask_app.main.user import user as user_blueprint
    from flask_app.main.car import car as car_blueprint
    from flask_app.api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(car_blueprint)
    app.register_blueprint(api_1_0_blueprint)  #url_prefix='/api/v1.0'
    return app




