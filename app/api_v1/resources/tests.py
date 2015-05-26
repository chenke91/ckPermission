from flask.ext.restful import Resource, reqparse

class Test(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser() 
        self.parser.add_argument('id', type=int)

        super(AccountAPI, self).__init__()

    def get(self):
        return {'id': id}

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass