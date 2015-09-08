#coding: utf-8

from flask import jsonify, request
from flask.ext.login import current_user
from app.exceptions import JsonOutputException
from app import db
from sqlalchemy.exc import IntegrityError
from ..auth.models import Role, Module
from . import admin

@admin.route('/roles/')
def roles():
    '''
    角色列表
    '''
    roles = Role.query.all()
    res = {
        "items": [role.to_dict() for role in roles]
    }
    return jsonify(res)

@admin.route('/roles/update/', methods=['POST'])
def update():
    '''
    新增/编辑用户
    '''
    name = request.json.get('name')
    permissions = request.json.get('permissions', 0)
    id = request.json.get('id')
    if not name:
        raise JsonOutputException('请输入用户名');
    if not id:
        role = Role(
            name=name,
            permissions=permissions)
        msg = '新增成功'
    else:
        role = Role.query.get_or_404(id)
        role.name = name
        role.permissions = permissions
        msg = '编辑成功'
    db.session.add(role)
    try:
        db.session.commit()
    except IntegrityError:
        raise JsonOutputException('该用户名已被使用')
    res = {'item': role.to_dict(), 'msg': msg}
    return jsonify(res)

@admin.route('/roles/modules/')
def roles_modules():
    '''
    模块列表
    '''
    items = Module.list()
    res = {'items': items}
    return jsonify(res)
