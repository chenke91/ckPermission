#coding: utf-8

from flask import request, abort, redirect, url_for
from flask.ext.login import current_user
from . import admin_blueprint

#权限验证
@admin_blueprint.before_request
def before_request():
    endpoint = request.endpoint
    if current_user.is_anonymous():
        return redirect(url_for('auth.login'))
    if not current_user.check_access(endpoint):
        abort(401)