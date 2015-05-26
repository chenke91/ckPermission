#encoding: utf-8
from .. import db

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    permissions = db.relationship('Permission', backref='admin', lazy="dynamic")


class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    pid = db.Column(db.Integer)
    is_show = db.Column(db.Boolean, default=True)
    action = db.Column(db.String(64), index=True)
    memo = db.Column(db.String(255))
    icon = db.Column(db.String(128))
    order = db.Column(db.Integer)
    status = db.Column(db.Integer)
    is_default = db.Column(db.Boolean, default=False)
    permissions = db.relationship('Permission', backref='module')

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    permissions = db.relationship('Permission', backref='role', lazy="dynamic")

class AdminRole(db.Model):
    __tablename__ = 'admin_roles'

    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer)
    rid = db.Column(db.Integer)

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer, db.ForeignKey('admins.id'))
    rid = db.Column(db.Integer, db.ForeignKey('roles.id'))
    mid = db.Column(db.Integer, db.ForeignKey('modules.id'))

