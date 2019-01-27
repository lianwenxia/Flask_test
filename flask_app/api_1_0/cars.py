from . import api
from .authentication import multi_auth, basic_auth
from flask_app.model.car import CarDetail, CarModel, CarParm
from flask import jsonify, request, abort, g
from flask_app import db
from .errors import forbidden, not_exit
from flask_app.main import main
from flask_login import current_user


@api.route('/car/')
def get_car():
    id = request.args.get('id')
    car = CarDetail.query.filter_by(id=id).first()
    if not car:
        return not_exit('查询的车辆不存在！')
    return jsonify({'car': car.to_json()})


@api.route('/cars/')
def get_cars():
    cars = CarDetail.query.all()
    print('***********users')
    return jsonify({'cars': [car.to_json() for car in cars] })


@api.route('/brand/')
def get_brand():
    pass


@api.route('/model/')
def get_model():
    id = request.args.get('id')
    car = CarModel.query.filter_by(id=id).first()
    if not car:
        return not_exit('查询的模型不存在！')
    return jsonify({'car': car.to_json()})


# 新增模型
@api.route('/model/post/', methods=['POST'])
def post_model():
    car_model = request.json.get('car_model')
    detail_id_list = request.json.get('detail') or None
    if detail_id_list:
        detail = []
        print('******new***********')
        try:
            for detail_id in detail_id_list:
                detail.append(CarDetail.query.filter_by(id=detail_id).first())
        except:
            detail.append(CarDetail.query.filter_by(id=detail_id_list).first())
        model = CarModel(car_model=car_model, detail=detail)
    else:
        model = CarModel(car_model=car_model)
    db.session.add(model)
    # db.session.commit()
    return jsonify({"status": 200})
    # return jsonify({'car': car.to_json()})


# 修改模型
@api.route('/model/<id>/put', methods=['PUT'])
def put_model(id):
    # print('***********************put')
    car = CarModel.query.filter_by(id=id).first()
    print(car.car_model)
    car_model = request.json.get('car_model') or car.car_model
    # print(car_model)

    detail_id_list = request.json.get('id') or None
    print(detail_id_list)
    if detail_id_list:
        detail = []
        print('******new***********')
        try:
            for detail_id in detail_id_list:
                detail.append(CarDetail.query.filter_by(id=int(detail_id)).first())
        except:
            detail.append(CarDetail.query.filter_by(id=detail_id_list).first())
        # car.detail = [detail]
    else:
        print('******old***********')
        detail = car.detail
    car.detail = detail
    car.car_model = car_model
    print(car)
    # db.session.add(model)
    # db.session.commit()
    return jsonify({"status": 200})
    # return jsonify({'car': car.to_json()})


@api.route('/model/<id>/del', methods=['DELETE'])
def del_model(id):
    model = CarModel.query.filter_by(id=id).first()
    db.session.delete(model)
    return jsonify({"status": 200})


@api.route('/models/')
def get_models():
    models = CarModel.query.all()
    return jsonify({'models': [model.to_json() for model in models]})


@api.route('/parm/')
def get_parm():
    pass


