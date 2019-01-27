from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask_app.model.user import User, AnonymousUser
from flask import g, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# from flask_login import AnonymousUserMixin


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)



@basic_auth.verify_password
def verify_password(email, password):
    user = None
    print('********in')
    # if email == '':
    #     print('emao', email)
    #     g.current_user = AnonymousUser()
    #     return True
    user = User.query.filter_by(email=email).first()
    # print(user)
    if not user:
        print('not ')
        return False
    g.current_user = user
    print('user is', user.username, user.password_hash)
    print(password, type(password))
    print(user.verify_password(password))
    # g.token = '123'
    return True

@token_auth.verify_token
def verify_token(token):
    # g.user = None
    print('**************innner token')
    print(token)
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        id = s.loads(token).get('id')
    except:
        return False
    # print(id)
    user = User.query.filter_by(id=int(id)).first()
    g.current_user = user
    print(user)
    if user:
        return True
    return False