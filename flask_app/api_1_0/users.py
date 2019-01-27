from . import api
from .authentication import multi_auth, basic_auth
from flask_app.model.user import User, AnonymousUser
from flask import jsonify, request, abort, g
from flask_app import db
from .errors import forbidden, not_exit
from flask_app.main import main
from flask_login import current_user


@api.route('/')
@basic_auth.login_required
def index():
    return "Hello, %s!" % basic_auth.username()



@api.route('/user/')
def get_user():
    idr = request.args.get('id')
    print('*************')
    print(idr)
    print('g', g.current_user)
    user = User.query.filter_by(id=idr).first()
    if not user:
        return not_exit('查询的用户不存在！')
    return jsonify({'users': user.to_json()})


@api.route('/users/')
def get_users():
    users = User.query.all()
    print('***********users')
    return jsonify({'users': [user.to_json() for user in users] })


@api.route('/users/post/<int:id>/', methods=['PUT'])
def put_user(id):
    # users = User.query.all()
    # print('***********users')
    print(id)
    user = User.query.filter_by(id=id).first()
    # user.email =
    username = request.json.get('username')
    # email = request.json.get('email')
    user.username = username
    # db.session.add(user)
    db.session.commit()
    # print(request.json.get('name'))
    return jsonify({'users': 'ok' })


@api.route('/users/post/', methods=['POST'])
def post_user():
    # users = User.query.all()
    # print('***********users')
    username = request.json.get('username')
    email = request.json.get('email')
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    print(request.json.get('name'))
    return jsonify({'users': 'ok' })


@api.before_request
@multi_auth.login_required
def before_request():
    if isinstance(g.current_user, AnonymousUser):
        print('*************anony')
        return forbidden(u'用户未认证或未登录')


@api.route('/token/')
@multi_auth.login_required
def get_auth_token():
    g.token = None
    print(g.current_user)
    if g.token:
        print('token already exit')
        return jsonify({'token': g.token.decode('ascii')})
    else:
        token = g.current_user.generate_auth_token(3600)
        g.token = token
        print('token does not exit')
        return jsonify({'token': token.decode('ascii')})