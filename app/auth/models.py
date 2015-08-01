#encoding: utf-8
from .. import db, cache

admin_role = db.Table(
    'admin_role',
    db.Column('admin_id', db.Integer, db.ForeignKey('admins.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
    )

class PermissionMixin(object):
    #添加权限
    def add_permission(self, module):
        self.permissions = int(self.permissions) | int(module.permission)
        cache.clear()
        db.session.add(self)
        db.session.commit()

    #删除权限
    def rm_permission(self, module):
        self.permissions = int(self.permissions) \
            & (int(self.permissions) ^ int(module.permission))
        cache.clear()
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
        key = '{id}_access_{action}'.format(id=self.id, action=action)
        res = cache.get(key)
        if res is None:
            module = Module.query.filter_by(action=action).first()
            if not module:
                res = False
            else:
                whole_permissions = self.__whole_permissions()
                res = bool(whole_permissions & int(module.permission))
            cache.set(key, res, 3600)
        return res

    #查询用户拥有权限的模块列表
    def module_list(self):
        whole_permissions = self.__whole_permissions()
        module_list = Module.query.\
            filter(Module.permission.op('&')(whole_permissions)).\
            order_by(Module.order).all()
        return modules_tree(module_list)

    def __repr__(self):
        return '<Admin: {id}>'.format(id=self.id)

class Role(db.Model, PermissionMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    permissions = db.Column(db.String(64), default=0)

    def __repr__(self):
        return '<Role: {id}>'.format(id=self.id)

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'pid': self.pid,
            'memo': self.memo,
            'icon': self.icon,
            'permission': self.permission
        }

    def __repr__(self):
        return '<Module: {id}>'.format(id=self.id)

def modules_tree(modules, pid=0):
    res = []
    for module in modules:
        if module.pid == pid:
            data = module.to_dict()
            data['sub_modules'] = modules_tree(modules, pid=module.id)
            res.append(data)
    return res

def generate_fake():
    db.session.rollback()
    db.drop_all()
    db.create_all()
    admin = Admin(
        email = 'admin@qq.com',
        name = 'admin'
    )
    role = Role(
        name = 'admin'
    )
    admin.roles.append(role)
    db.session.add(admin)
    db.session.commit()
    module1 = Module(
        name = '用户管理',
        action = 'main.user',
        permission = 2
    )
    module2 = Module(
        name = '权限管理',
        action = 'main.permission',
        permission = 4
    )
    db.session.add(module1)
    db.session.add(module2)
    db.session.commit()
    role.add_permission(module1)
    role.add_permission(module2)
