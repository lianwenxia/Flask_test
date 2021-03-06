from flask_app import db, file_path
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .. import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
import datetime
from . import BaseModelview
from flask_admin import form
from jinja2 import Markup
from sqlalchemy.event import listens_for
from random import seed
import forgery_py
from sqlalchemy.exc import IntegrityError


# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#
# class Permission:
#     FOLLOW = 0x01
#     COMMENT = 0x02
#     WRITE_ARTICLES = 0x04
#     MODERATE_COMMENTS = 0x08
#     ADMINISTER = 0x80


class User(UserMixin, db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, index=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(11), unique=True)
    location = db.Column(db.String(100), default=False)
    real_name = db.Column(db.String(100), default=False)
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    profile_picture = db.Column(db.String(100), default=False)
    is_administrator = db.Column(db.Boolean, default=False)

    # 将password方法变成属性
    @property
    def password(self):
        raise AttributeError('password 不是一个可读属性')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成和检验令牌
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)

        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True

        db.session.add(self)
        db.session.commit()
        return True


    def ping(self):
        self.last_seen = datetime.datetime.utcnow()
        db.session.add(self)
        return self.last_seen

    @staticmethod
    def generate_fake(count=50):
        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     real_name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     # about_me=forgery_py.lorem_ipsum.sentence(),
                     last_seen=forgery_py.date.date(True))
            print('***************')
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'email': self.email,
            'last_seen': self.last_seen,
            'location': self.location,
            'real_name': self.real_name
        }

        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)

        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<username %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# admin View视图渲染
class UserModelview(BaseModelview):

    # 显示的列
    column_list = ('id', 'profile_picture', 'username', 'email', 'confirmed', 'is_administrator', 'phone')
    # column_filters = ('password_hash', )

    # 设置缩略图的
    def _list_thumbnail(view, context, model, name):
        if not model.profile_picture:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.profile_picture)))

    # 格式化列表的图像显示
    column_formatters = {
        'profile_picture': _list_thumbnail
    }
    # 扩展列表显示的头像为60*60像素
    form_extra_fields = {
        'profile_picture': form.ImageUploadField('Image',
                                                 base_path=file_path,
                                                 relative_path='save/',
                                                 thumbnail_size=(60, 60, True))
    }


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser