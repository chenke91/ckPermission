#coding: utf-8

from flask import jsonify, request, abort
from flask.ext.login import current_user
from app import db
from app.exceptions import JsonOutputException
from ..auth.models import Module
from . import admin

@admin.route('/modules/')
def modules():
    items = Module.list()
    res = {'items': items}
    return jsonify(res)