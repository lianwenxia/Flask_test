from flask_app import db, file_path
from . import BaseModelview
from flask_admin import form
from jinja2 import Markup
from flask import url_for
from sqlalchemy.event import listens_for

# 车辆参数
class CarParm(db.Model):

    __tablename__ = 'parm'
    id = db.Column(db.Integer, primary_key=True)
    detail = db.relationship('CarDetail', backref='parm')
    # 长宽高
    L_W_H = db.Column(db.String(20), nullable=True)
    # 前 / 后轮距
    front_rear_wheelbase = db.Column(db.String(20), nullable=True)
    # 前 / 后悬长度
    suspension_length = db.Column(db.String(20), nullable=True)
    # 轴距
    wheelbase = db.Column(db.Numeric(10), nullable=True)
    # 风阻系数(cd)
    cd = db.Column(db.Numeric(10), nullable=True)
    # 整备质量(kg)
    quality = db.Column(db.Numeric(10), nullable=True)
    # 油箱容积
    Fuel_tank_capacity = db.Column(db.Numeric(10), nullable=True)
    # 行李箱容积
    cargo_volume = db.Column(db.Numeric(10), nullable=True)
    # 最大行李箱容积
    max_cargo_volume = db.Column(db.Numeric(10), nullable=True)
    # 车门数(含后车门)
    door_num = db.Column(db.Integer, nullable=True)
    # 乘员数(含驾驶员)
    occupants_num = db.Column(db.Integer, nullable=True)
    def __repr__(self):
        return '<id %r>' % self.id


# 品牌
class BrandModel(db.Model):

    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    detail = db.relationship('CarDetail', backref='brand')
    # 品牌
    brand = db.Column(db.String(20))
    def __repr__(self):
        return '<brand %r>' % self.brand


# 车型
class CarModel(db.Model):

    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    detail = db.relationship('CarDetail', backref='model')
    # 车型
    car_model = db.Column(db.String(20))
    def __repr__(self):
        return '<model %r>' % self.car_model


class CarDetail(db.Model):

    __tablename__ = 'detail'
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    parm_id = db.Column(db.Integer, db.ForeignKey('parm.id'))
    # 车名
    car_name = db.Column(db.String(50))
    # 价格
    price = db.Column(db.Numeric(10), nullable=True)
    # 上牌日
    register = db.Column(db.Date, nullable=True)
    # 里程
    mileage = db.Column(db.Numeric(10), nullable=True)
    # 年检有效期
    annual_inspection = db.Column(db.Date, nullable=True)
    # 保险有效期
    insurance = db.Column(db.Date, nullable=True)
    # 看车地址
    car_addr = db.Column(db.String(100), nullable=True)
    # 车龄
    car_age = db.Column(db.String(20), nullable=True)
    # 图片
    # img = db.Column(db.LargeBinary(length=2048))
    img = db.relationship('CarImage', backref='detail')
    def __repr__(self):
        return '<name %r>' % self.car_name


class CarImage(db.Model):
    __tablename__ = 'img'
    id = db.Column(db.Integer, primary_key=True)
    detail_id = db.Column(db.Integer, db.ForeignKey('detail.id'))
    img = db.Column(db.String(100))
    # img = db.Column(db.String(100))
    def __repr__(self):
        return '<detail_id %r>' % self.detail_id


# admin View视图渲染
class ImgModelview(BaseModelview):

    # 设置缩略图的
    def _list_thumbnail(view, context, model, name):
        if not model.img:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.img)))

    # 格式化列表的图像显示
    column_formatters = {
        'img': _list_thumbnail
    }
    # 扩展列表显示的头像为60*60像素
    form_extra_fields = {
        'img': form.ImageUploadField('CarImage',
                                     base_path=file_path,
                                     relative_path='carimg/',
                                     thumbnail_size=(60, 60, True))
    }
