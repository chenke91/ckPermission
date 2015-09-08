#coding: utf-8

from flask import jsonify, request, abort, url_for
from flask.ext.login import current_user
from app import db
from app.exceptions import JsonOutputException
from ..auth.models import Module
from . import admin
from .forms import ModuleFrom
from sqlalchemy.exc import IntegrityError
import importlib

@admin.route('/modules/')
def modules():
    '''
    模块列表
    '''
    items = Module.list()
    res = {'items': items}
    return jsonify(res)

@admin.route('/modules/load/')
def load_permission():
    '''
    载入权限
    '''
    Module.load()
    return jsonify({})

@admin.route('/modules/add/', methods=['POST'])
def add_module():
    '''
    新增/编辑
    '''
    id = request.json.get('id')
    form = ModuleFrom()
    if form.validate_on_submit():
        #新增
        if not id:
            module = Module(
                name=form.name.data,
                pid=form.pid.data,
                order=form.order.data or '',
                icon=form.icon.data or '',
                permission=Module.get_next_permission())
            msg = '新增成功'
        else:
            module = Module.query.get_or_404(id)
            module.name = form.name.data
            module.pid = form.pid.data
            module.order = form.order.data or ''
            module.icon = form.icon.data or ''
            msg = '编辑成功'
        if not form.pid.data == '0':
            module.url=form.url.data
        else:
            module.level = 1
        db.session.add(module)
        try:
            db.session.commit()
            return jsonify({'msg': msg})
        except IntegrityError:
            db.session.rollback()
            raise JsonOutputException('模块名称或url已存在')
    for errors in form.errors.values():
        for error in errors:
            raise JsonOutputException(error)
    raise JsonOutputException('请求失败')

@admin.route('/modules/masters/')
def get_master():
    '''
    获取主菜单
    '''
    masters = Module.query.filter_by(pid=0).all()
    items = [master.to_dict() for master in masters]
    data = [{'id': 0, 'name': '请选择主菜单'}]
    data.extend(items)
    res = {'items': data}
    return jsonify(res)