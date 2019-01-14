from flask import request
from flask import render_template
from flask_app import app, db
from flask_script import Manager, Server
from flask_app.model.car import CarModel, CarDetail, BrandModel
manager = Manager(app)
# @manager.command
@app.route('/')
def index():
    return render_template('index.html')
    # user_agent = request.headers.get('user-agent')
    # return '这是该网页的user agent：%s' % user_agent

@app.route('/hello<name>/')
def hello(name):
    return '<h1>Hello %s!</h1>' % name


if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    # img = open('D:/py3/ppp/img/3.jpg', 'rb')
    # carB = BrandModel(id=1, brand='宝马')
    # car = CarDetail(id=1, car_name='123')
    # carB.detail.append(car)
    # db.session.add(carB)
    # db.session.commit()
    car = CarDetail.query.filter_by(id=1)
    print(car)
    manager.run()
