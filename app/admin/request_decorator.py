#coding: utf-8

from flask import request, abort, redirect, url_for
from flask.ext.login import current_user
from . import admin

#权限验证
@admin.before_request
def before_request():
    ignore = ['admin.menu']
    endpoint = request.endpoint
    if endpoint not in ignore:
        if current_user.is_anonymous():
            return redirect(url_for('auth.login'))
        if not current_user.check_access(endpoint):
            abort(401)