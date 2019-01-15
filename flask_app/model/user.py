from flask_app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<username %r>' % self.username


from .. import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
