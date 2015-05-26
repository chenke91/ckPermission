#encoding: utf-8
from . import auth

@auth.route('/')
def test():
    return 'hello'