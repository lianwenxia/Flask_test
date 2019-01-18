from flask_app import db, create_app
from flask_script import Manager, Server
from flask_app.model.car import CarModel, CarDetail, BrandModel
from flask_migrate import Migrate, MigrateCommand
import os
from flask_app.model import user

app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
