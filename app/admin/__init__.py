#encoding: utf-8
from flask import Blueprint, render_template
from flask.ext.login import login_required

admin = Blueprint('admin', __name__)

from . import menus, request_decorator, user, role
