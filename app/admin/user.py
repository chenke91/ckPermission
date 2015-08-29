#coding: utf-8

from flask import jsonify, request
from flask.ext.login import current_user
from ..auth.models import Admin
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