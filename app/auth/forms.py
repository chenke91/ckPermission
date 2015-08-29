#coding=utf-8

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo

class LoginFrom(Form):
    email = StringField('邮箱',
        validators=[Required('请输入邮箱地址'), Email('邮箱格式不正确')])
    password = PasswordField('密码',
        validators=[Required('请输入密码'), Length(6, 20, '密码长度为6~20')])
    submit = SubmitField('登陆')