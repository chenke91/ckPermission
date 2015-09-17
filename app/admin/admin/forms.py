#coding=utf-8

from flask.ext.wtf import Form
from wtforms import StringField, SelectField, IntegerField, ValidationError
from wtforms.validators import Required, Email, Length, EqualTo
from app.auth.models import Module

class ModuleFrom(Form):
    name = StringField('name',
        validators=[Required('请输入模块名称')])
    pid = SelectField('master')
    url = StringField('url')
    icon = StringField('icon')
    order = IntegerField('order')

    def __init__(self, *args, **kwargs):
        super(ModuleFrom, self).__init__(*args, **kwargs)
        masters = Module.query.filter_by(pid=0).all()
        res = [master.to_dict() for master in masters]
        choice = list(zip(map(lambda x: str(x['id']), res), map(lambda x: x['name'], res)))
        self.pid.choices = [('0', '')]
        self.pid.choices.extend(choice)

    def validate_url(self, field):
        if not self.pid.data=='0' and not field.data:
            raise ValidationError('请输入url')

    def validate_icon(self, field):
        if not self.pid.data=='0' and not field.data:
            raise ValidationError('请选择图标')
