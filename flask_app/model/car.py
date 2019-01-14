from flask_app import db


class CarModel(db.Model):

    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True)
    detail = db.relationship('CarDetail', backref='carmodel')
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
        return '<Id %r>' % self.id



class CarDetail(db.Model):
    __tablename__ = 'detail'
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
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
    img = db.Column(db.LargeBinary(length=2048))
    def __repr__(self):
        return '<Id %r>' % self.id

class BrandModel(db.Model):

    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    detail = db.relationship('CarDetail', backref='brand')
    # 品牌
    brand = db.Column(db.String(20))
    # 车型
    car_model = db.Column(db.String(20))
    def __repr__(self):
        return '<Id %r>' % self.brand