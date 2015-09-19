#coding:utf-8

import os
from flask import current_app
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db

app = create_app(os.getenv('BLOG_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    '''run the unit test'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def init_app():
    from app.auth.models import init_auth
    init_auth()

@manager.command
def compilejs():
    from app.bin.compilejs import compile
    folder = current_app.config['JS_FOLDER']
    includes = current_app.config['JS_CPL_INCLUDES']
    compile(folder, includes)


if __name__ == '__main__':
    manager.run()