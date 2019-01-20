from flask_app import db, create_app, admin
from flask_script import Manager, Server
from flask_app.model.car import CarModel, CarDetail, BrandModel, CarImage, CarParm, ImgModelview
from flask_migrate import Migrate, MigrateCommand
import os
from flask_app.model import BaseModelview
from flask_app.model.user import User, UserModelview
# from flask_admin import Admin, BaseView, expose


app = create_app('development')
admin.add_view(UserModelview(User, db.session, name=u'用户管理'))
admin.add_view(BaseModelview(CarParm, db.session, name=u'车辆参数'))
admin.add_view(BaseModelview(BrandModel, db.session, name=u'品牌'))
admin.add_view(ImgModelview(CarImage, db.session, name=u'车辆图片'))
admin.add_view(BaseModelview(CarModel, db.session, name=u'车型'))
admin.add_view(BaseModelview(CarDetail, db.session, name=u'车辆细节管理'))
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
# manager.add_view()



if __name__ == "__main__":
    manager.run()
