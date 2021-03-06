#coding: utf-8

from flask import jsonify, request, abort
from flask.ext.login import current_user
from app import db
from app.exceptions import JsonOutputException
from app.auth.models import Admin, Role
from .. import admin_blueprint

@admin_blueprint.route('/users/')
def users():
    '''
    用户列表
    '''
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

@admin_blueprint.route('/users/<int:id>/')
def get_user(id):
    '''
    获取用户
    '''
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
    return jsonify(data)

@admin_blueprint.route('/users/new/', methods=['GET', 'POST'])
def new_user():
    '''
    新增
    '''
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    role_ids = request.json.get('role_ids', [])
    if Admin.query.filter_by(email=email).first():
        raise JsonOutputException('该邮箱已被使用')
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

@admin_blueprint.route('/users/update/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    '''
    更新
    '''
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    role_ids = request.json.get('role_ids', [])
    exist = Admin.query.filter_by(email=email).first()
    if not exist.id == id:
        raise JsonOutputException('该邮箱已被使用')
    user = Admin.query.get_or_404(id)
    user.name = name
    user.email = email
    if password:
        user.password = password
    old_roles = user.roles.all()
    new_roles = [Role.query.get(id) for id in role_ids]
    delete_roles = list(set(old_roles).difference(set(new_roles)))
    add_roles = list(set(new_roles).difference(set(old_roles)))
    for role in delete_roles:
        user.roles.remove(role)
    for role in add_roles:
        user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    res = {'status': 0}
    return jsonify(res)

@admin_blueprint.route('/users/delete_toggle/<int:id>/')
def delete_toggle(id):
    '''
    删除
    '''
    user = Admin.query.get_or_404(id)
    user.avalible = not user.avalible
    db.session.add(user)
    db.session.commit()
    res = {'id': user.id, 'avalible': user.avalible}
    return jsonify(res)

