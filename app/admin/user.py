#coding: utf-8

from flask import jsonify, request, abort
from flask.ext.login import current_user
from app import db
from ..auth.models import Admin, Role
from . import admin

@admin.route('/users/')
def users():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    pagination = Admin.query\
        .paginate(page, per_page, error_out=False)
    items = [item.to_dict() for item in pagination.items]
    res = {
        "items": items,
        'total': pagination.total
    }
    return jsonify(res)

@admin.route('/users/<int:id>/')
def get_user(id):
    user = Admin.query.get_or_404(id)
    data = user.to_dict()
    roles = Role.query.all()
    user_roles = []
    user_role_ids = list(map(lambda x: x['id'], data['roles']))
    for role in roles:
        tmp = role.to_dict()
        if role.id in user_role_ids:
            tmp['selected'] = True
        user_roles.append(tmp)
    data['user_roles'] = user_roles
    res = {'status': 0, 'data': data}
    return jsonify(res)

@admin.route('/users/new/', methods=['GET', 'POST'])
def new_user():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    role_ids = request.json.get('role_ids', [])
    if Admin.query.filter_by(email=email).first():
        res = {'status': 1, 'msg': '该邮箱已被使用'}
        return jsonify(res)
    admin = Admin(
        name = name,
        email = email,
        password = password)
    for role_id in role_ids:
        role = Role.query.get(role_id)
        admin.roles.append(role)
    db.session.add(admin)
    db.session.commit()
    res = {'status': 0}
    return jsonify(res)