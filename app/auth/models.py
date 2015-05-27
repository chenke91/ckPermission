#encoding: utf-8
from .. import db

admin_role = db.Table(
    'admin_role',
    db.Column('admin_id', db.Integer, db.ForeignKey('admins.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
    )

class PermissionMixin(object):
    #添加权限
    def add_permission(self, module):
        self.permissions = int(self.permissions) | int(module.permission)
        db.session.add(self)
        db.session.commit()

    #删除权限
    def rm_permission(self, module):
        self.permissions = int(self.permissions) \
            & (int(self.permissions) ^ int(module.permission))
        db.session.add(self)
        db.session.commit()


class Admin(db.Model, PermissionMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    permissions = db.Column(db.String(64), default=0)
    roles = db.relationship('Role',
                            secondary=admin_role,
                            backref=db.backref('admins', lazy='dynamic'),
                            lazy='dynamic')

    #获取用户所有权限，包括自身权限与角色权限
    def __whole_permissions(self):
        permissions = int(self.permissions)
        for role in self.roles.all():
            permissions |= int(role.permissions)
        return permissions

    #验证某个路由的权限
    def check_access(self, action):
        module = Module.query.filter_by(action=action).first()
        if not module:
            return False
        whole_permissions = self.__whole_permissions()
        return bool(whole_permissions & int(module.permission))

class Role(db.Model, PermissionMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    permissions = db.Column(db.String(64), default=0)

class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    pid = db.Column(db.Integer, default=0)
    is_show = db.Column(db.Boolean, default=True)
    action = db.Column(db.String(64), unique=True, index=True)
    memo = db.Column(db.String(255))
    icon = db.Column(db.String(128))
    order = db.Column(db.Integer)
    status = db.Column(db.Integer)
    is_default = db.Column(db.Boolean, default=False)
    permission = db.Column(db.String(64), unique=True)


