#coding: utf-8

from flask import jsonify
from flask.ext.login import current_user
from .. import admin_blueprint

@admin_blueprint.route('/menus/')
def menu():
    modules = current_user.module_list()
    res = {'modules': modules}
    return jsonify(res)

@admin_blueprint.route('/current_user/')
def current_user_view():
    res = current_user.to_dict()
    return jsonify(res);