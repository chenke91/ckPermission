#coding: utf-8

from flask import jsonify
from flask.ext.login import current_user
from . import admin

@admin.route('/menus/')
def menu():
    modules = current_user.module_list()
    res = {'modules': modules}
    return jsonify(res)