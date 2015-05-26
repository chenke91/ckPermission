from decimal import Decimal
import datetime
import re

__all__ = [
    "boolean",
    "date_validator",
    'int_',
    "inargs",
    "is_number"
]

def boolean(value):
    if value == '0' or value == "False" or value == "false" or\
            value is False or value == 0:
        return False
    if value == '':
        return None
    return True

def date_validator(date):
    if not date:
        return None
    try:
        y, m, d = map(int, date.split('-'))
        return datetime.date(y, m, d)
    except:
        raise Exception("Unexcept date format.")

#验证传入参数是否在指定参数中
def inargs(*args, types=str):
    def func(value):
        value =types(value)
        if value not in args:
            raise Exception("Unexcept value.")
        return value
    return func

#验证账号
def account_validate(value):
    pattern = r'^[-0-9a-zA-Z]{0,32}$'
    if not re.match(pattern, value):
        raise Exception('unvalidate formate')
    return value

#验证金额
def amount_validate(value):
    try:
        amount = Decimal(str(value))
    except:
        raise Exception('unvalidate formate')
    if amount <= 0:
        raise Exception('不可以是负数或0')
    return amount

#验证传入参数是否是纯数字 返回原字符串
def is_number(value):
    int(value)
    return value

def int_(value):
    try:
        return int(value)
    except:
        pass