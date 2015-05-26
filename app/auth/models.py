#encoding: utf-8
from .. import db

admin_role = db.Table(
    'admin_role',
    db.Column('admin_id', db.Integer, db.ForeignKey('admins.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
    )

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    permissions = db.relationship('Permission', backref='admin', lazy="dynamic")
    roles = db.relationship('Role',
                            secondary=admin_role,
                            backref=db.backref('roles', lazy='dynamic'))

    ##验证某个路由的权限
    # def check_access(action):
    #     module = Module.query.filter_by(action=action).first()
    #     if not module:
    #         return False

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    permissions = db.relationship('Permission', backref='role', lazy="dynamic")
    admins = db.relationship('Admin',
                            secondary=admin_role,
                            backref=db.backref('admins', lazy='dynamic'))


class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    pid = db.Column(db.Integer)
    is_show = db.Column(db.Boolean, default=True)
    action = db.Column(db.String(64), unique=True, index=True)
    memo = db.Column(db.String(255))
    icon = db.Column(db.String(128))
    order = db.Column(db.Integer)
    status = db.Column(db.Integer)
    is_default = db.Column(db.Boolean, default=False)
    permissions = db.relationship('Permission', backref='module')

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer, db.ForeignKey('admins.id'))
    rid = db.Column(db.Integer, db.ForeignKey('roles.id'))
    mid = db.Column(db.Integer, db.ForeignKey('modules.id'))

