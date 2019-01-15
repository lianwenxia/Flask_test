from flask import request, flash, redirect, url_for
from flask import render_template
from . import user
from flask_script import Manager, Server
from .forms import LoginForm, RegisterForm
from ...model.user import User
from flask_login import login_user, login_required, logout_user, login_required
from flask_app import db
from flask_mail import Message
from flask_app import mail
from flask_app import config
@user.route('/')
def index():

    return render_template('user/index.html')


@user.route('/secret')
@login_required
def secret():

    return 'Only authenticated users are allowed!'


@user.route('/login/', methods=('GET', 'POST'))
def login():
    name = None
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user, form.remember_me.data)
            return redirect(url_for('user.index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form, name=name)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@user.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        msg = Message("Hello Flask", sender="1213284679@qq.com", recipients=[form.email.data])
        msg.body = '欢迎您的注册！'
        mail.send(msg)
        flash('You can now login.')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)

