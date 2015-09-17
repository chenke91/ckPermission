#encoding: utf-8
from flask import Blueprint, render_template
from flask.ext.login import login_required

admin_blueprint = Blueprint('admin', __name__)

from . import request_decorator
from .admin import public, users, roles, modules
