from . import api

from .resources.tests import Test

# 添加路由
api.add_resource(Test, '/tests')