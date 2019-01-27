import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '\xf4T\x00\x14\x06I\xf2\xa7\xa5\x98\xcef\x01e\xc3\xc5\xce\xd6\xd3\x8bL\xef\x16'
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'



    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    DEBUG = True
    # 邮箱
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  #'1213284679@qq.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')  #'1213284679@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  #'kihknzbjpueubaba'
    UPLOAD_FOLDER = r'D:\web_flask\flask_app\static\save'
    CAR_UPLOAD = r'D:\web_flask\flask_app\static\carimg'

    # 数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True # Flask - SQLAlchemy 2.0以前使用
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # Flask - SQLAlchemy 2.0以后使用

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/flask_test'

    # jsonify的字符串在web显示中文
    JSON_AS_ASCII = False


class TestingConfig(Config):
    TESTING = True
    # mysql + pymysql: // root: 123456 @ localhost / flask_test_test
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
