from flask_app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .. import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import datetime


class User(UserMixin, db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    # password = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(11), unique=True)
    location = db.Column(db.String(100), default=False)
    real_name = db.Column(db.String(10), default=False)
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    profile_picture = db.Column(db.String(100), default=False)


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

    def __repr__(self):
        return '<username %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


