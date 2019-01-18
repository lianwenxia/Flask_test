from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ...model.user import User
from wtforms import ValidationError


class NameForm(FlaskForm):
    name = StringField('what is your name?', validators=[DataRequired()])
    password = PasswordField('what is your password?', validators=[DataRequired()])
    login = SubmitField('login')
    logout = SubmitField('logout')


class LoginForm(FlaskForm):

    username = StringField('username: ', validators=[DataRequired()])
    password = PasswordField('password: ', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):

    email = StringField('email_addr: ',
                        validators=[DataRequired(), Length(1, 64), Email()])

    username = StringField('username: ',
                           validators=[DataRequired(), Length(1, 64),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                    '用户名要以字母开头！')])

    password = PasswordField('password: ',
                           validators=[DataRequired(),
                                       EqualTo('comfirm_password', message='密码输入不一致！')])
    comfirm_password = PasswordField('comfirm: ', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditForm(FlaskForm):
    real_name = StringField('realname: ', validators=[DataRequired()])
    phone = StringField('phone: ', validators=[DataRequired()])
    username = StringField('username: ', validators=[Length(1, 64)])
    email = StringField('email: ', validators=[Length(1, 64)])
    location = StringField('address: ', validators=[Length(1, 64)])
    submit = SubmitField('Modify')


class ProfileForm(FlaskForm):
    profile_picture = FileField('profile picture: ', validators=[DataRequired()])
    submit = SubmitField('Submit')




def validate_email(self, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')


def validate_username(self, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username already in use.')
