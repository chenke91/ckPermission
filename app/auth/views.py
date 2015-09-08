#encoding: utf-8
from flask import redirect, render_template, request, url_for, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from . import auth
from .forms import LoginFrom
from .models import Admin

@auth.route('/')
def test():
    return 'hello'

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous():
        return redirect('/#/')
    form = LoginFrom()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or '/#/')
        flash('password error')
    return render_template('admin/login.html', form=form)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('auth.login'))
