#encoding: utf-8
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import AnonymousUserMixin
from sqlalchemy import func
from .. import db, cache, login_manager
import importlib

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
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64), index=True)
    permissions = db.Column(db.String(64), default=0)
    avalible = db.Column(db.Boolean, default=True)
    roles = db.relationship('Role',
                            secondary=admin_role,
                            backref=db.backref('admins', lazy='dynamic'),
                            lazy='dynamic')

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @property
    def password(self):
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


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
                res = True
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
            filter(Module.is_show==True).\
            order_by(Module.order).all()
        return modules_tree(module_list)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'permissions': self.__whole_permissions(),
            'avalible': self.avalible,
            'roles': [role.to_dict() for role in self.roles.all()]
        }

    @staticmethod
    def generate_fake(role, count=20):
        from random import seed, uniform, choice
        import forgery_py
        seed()
        for i in range(count):
            admin = Admin(
                name = forgery_py.name.full_name(),
                password = '123456',
                email = forgery_py.internet.email_address()
            )
            admin.roles.append(role)
            db.session.add(admin)
        db.session.commit()

    def __repr__(self):
        return '<Admin: {id}>'.format(id=self.id)

class Role(db.Model, PermissionMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    permissions = db.Column(db.String(64), default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'permissions': self.permissions
        }

    @staticmethod
    def generate_fake(count=6):
        from random import seed, uniform, choice
        import forgery_py
        seed()
        for i in range(count):
            role = Role(
                name = forgery_py.name.full_name(),
                permissions = choice([2,4,8,16,10,12,14,6,26])
            )
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role: {id}>'.format(id=self.id)

class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    pid = db.Column(db.Integer, default=0)
    is_show = db.Column(db.Boolean, default=True)
    action = db.Column(db.String(64), unique=True, index=True)
    url = db.Column(db.String(64), unique=True)
    memo = db.Column(db.String(255))
    icon = db.Column(db.String(128))
    order = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=1)
    level = db.Column(db.Integer, default=2) #模块等级 1一级模块 2二级 3三级
    is_default = db.Column(db.Boolean, default=False)
    permission = db.Column(db.Integer)

    @staticmethod
    def list():
        modules = Module.query.all()
        return modules_tree(modules)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'pid': str(self.pid),
            'memo': self.memo,
            'icon': self.icon,
            'permission': self.permission,
            'url': self.url,
            'action': '/' + self.action.replace('.', '/') if self.action else ''
        }

    @staticmethod
    def load():
        load_modules = Module.query.\
            filter_by(level=2).\
            all()
        for module in load_modules:
            if not module.url:
                continue
            import_module_name = 'app.admin' + module.url.replace('/', '.')
            try:
                m = importlib.import_module(import_module_name)
            except:
                continue
            blueprint = 'admin'
            for view_func in m.__dir__():
                if view_func.startswith('__') or not\
                        callable(getattr(m, view_func)) or not\
                        getattr(m, view_func).__module__ == m.__name__:
                    continue
                action = '.'.join([blueprint, view_func])
                if Module.query.filter_by(action=action).first():
                    continue
                doc = getattr(m, view_func).__doc__ or ''
                module_obj = Module(
                    name='-'.join((doc.strip(),view_func)),
                    permission=module.permission,
                    action=action,
                    pid=module.id,
                    is_show=False,
                    level=3)
                db.session.add(module_obj)
        db.session.commit()

    @staticmethod
    def get_next_permission():
        max_permission = db.session.query(func.max(Module.permission)).scalar()
        return max_permission * 2

    def __repr__(self):
        return '<Module: {id}>'.format(id=self.id)

class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))

login_manager.anonymous_user = AnonymousUser

def modules_tree(modules, pid=0):
    res = []
    for module in modules:
        if module.pid == pid:
            data = module.to_dict()
            data['sub_modules'] = modules_tree(modules, pid=module.id)
            data['has_sub'] = False
            if len(data['sub_modules']) > 0:
                data['has_sub'] = True
            res.append(data)
    return res

def init_auth():
    db.session.rollback()
    db.drop_all()
    db.create_all()
    admin = Admin(
        email = 'chenke91@qq.com',
        name = 'admin',
        password = '123456'
    )
    role = Role(
        name = 'admin',
        permissions = 65535
    )
    admin.roles.append(role)
    db.session.add(admin)
    db.session.commit()
    sys_moduel = Module(
        name = '系统管理',
        permission = 2,
        level = 1)

    db.session.add(sys_moduel)
    db.session.commit()
    user_module = Module(
        name = '用户管理',
        icon = 'fa fa-user',
        url = '/admin/users',
        permission = 4,
        pid = sys_moduel.id)

    role_module = Module(
        name = '角色管理',
        icon = 'fa fa-sitemap',
        url = '/admin/roles',
        permission = 8,
        pid = sys_moduel.id)

    menu_module = Module(
        name = '模块管理',
        url = '/admin/modules',
        permission = 16,
        icon = 'fa fa-th',
        pid = sys_moduel.id)

    icon_module = Module(
        name = 'icons',
        url = '/admin/icons',
        permission = 32,
        icon = 'fa fa-leaf',
        pid = sys_moduel.id)

    db.session.add(user_module)
    db.session.add(role_module)
    db.session.add(menu_module)
    db.session.add(icon_module)
    db.session.commit()
    Module.load()
