#encoding: utf-8
import os
from flask import render_template, request, current_app, send_file
from flask.ext.login import login_required, current_user
from . import main

@main.route('/')
@login_required
def index():
    return render_template('admin/base.html')