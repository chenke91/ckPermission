#encoding: utf-8
from .. import db

admin_role = db.Table(
    'admin_role',
    db.Column('admin_id', db.Integer, db.ForeignKey('admins.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
    )

permissions = db.Table(
    'permissions',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('admin_id', db.Integer, db.ForeignKey('admins.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('module_id', db.Integer, db.ForeignKey('modules.id'))
    )

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    roles = db.relationship('Role',
                            secondary=admin_role,
                            backref=db.backref('admins', lazy='dynamic'),
                            lazy='dynamic')
    modules = db.relationship('Module',
                            secondary=permissions,
                            backref=db.backref('admins', lazy='dynamic'),
                            lazy='dynamic')

    # 获得管理员的所有权限
    def __whole_modules(self):
        modules = self.modules.all()
        for role in self.roles.all():
            modules += role.modules.all()
        return list(set(modules))

    #验证某个路由的权限
    def check_access(self, action):
        module = Module.query.filter_by(action=action).first()
        if module and module in self.__whole_modules():
            return True
        return False


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    modules = db.relationship('Module',
                            secondary=permissions,
                            backref=db.backref('roles', lazy='dynamic'),
                            lazy='dynamic')


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


