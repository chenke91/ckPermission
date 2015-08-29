#coding: utf-8

from flask import jsonify, request
from flask.ext.login import current_user
from ..auth.models import Role
from . import admin

@admin.route('/roles/')
def roles():
    roles = Role.query.all()
    res = {
        "items": [role.to_dict() for role in roles]
    }
    return jsonify(res)