from flask import request, flash, redirect, url_for
from flask import render_template, abort, current_app
from . import user
from flask_script import Manager, Server
from .forms import LoginForm, RegisterForm, EditForm, ProfileForm
from ...model.user import User
from flask_login import login_user, login_required, logout_user, login_required, current_user
from flask_app import db
from flask_mail import Message
from flask_app import mail
from flask_app import config
from flask_app.email import send_email
import os


@user.route('/')
def index():

    return render_template('index.html')


@user.route('/userinfo/')
@login_required
def userinfo():

    return render_template('user/userinfo.html')


@user.route('/edit/', methods=('GET', 'POST'))
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        current_user.real_name = form.real_name.data
        current_user.phone = form.phone.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.location = form.location.data

        # db.session.add(current_user)

        return redirect(url_for('.userinfo', username=current_user.username))
    form.real_name.data = current_user.real_name
    form.phone.data = current_user.phone
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.location.data = current_user.location
    return render_template('user/edit.html', form=form)


# 更换头像
@user.route('/pro_edit/', methods=('GET', 'POST'))
@login_required
def pro_edit():
    form = ProfileForm()

    if form.validate_on_submit():
        file = request.files['profile_picture']
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
        current_user.profile_picture = '/static/save/'+file.filename
        return redirect(url_for('.userinfo'))
    return render_template('user/pro_edit.html', form=form)


@user.route('/login/', methods=('GET', 'POST'))
def login():
    name = None
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('user.index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form, name=name)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('user.index'))


@user.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        # send_email(to=user.email, subject='Hello Flask',
        #            template='user/welcome', user_obj=user, token=token)
        flash('You can now login.')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)



@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('user.index'))

    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@user.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
