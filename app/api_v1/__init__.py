import json
from flask import Blueprint, make_response
from flask.ext.restful import Api
from app.exceptions import UserAlreadyExistsException


class MyApi(Api):
    def handle_error(self, e):
        if isinstance(e, UserAlreadyExistsException):
            code = 409
            data = {'status_code': code, 'message': "用户名已存在"}
        else:
            return super(MyApi, self).handle_error(e)
        return self.make_response(data, code)

api_blueprint = Blueprint('api', __name__)
# api = MyApi(app=api_blueprint, decorators=[login_required])
api = MyApi(app=api_blueprint)


#禁用缓存
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {'Cache-Control': 'no-cache', 
       'Pragma': 'no-cache',
       'Expires': 'Mon, 26 Jul 1997 05:00:00 GMT'})
    return resp

from . import routes