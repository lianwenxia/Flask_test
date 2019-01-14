from flask import Flask
app = Flask(__name__)
# from flask_app import views
from flask_sqlalchemy import SQLAlchemy

#加载配置文件内容
app.config.from_object('flask_app.settings')     #模块下的setting文件名，不用加py后缀
# app.config.from_envvar('FLASKR_SETTINGS')   #环境变量，指向配置文件setting的路径

#创建数据库对象
db = SQLAlchemy(app)

from flask_app.model.car import CarModel, BrandModel, CarDetail