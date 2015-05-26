#coding=utf8
import time
import math

#分页
def paginate(query, page, per_page):
    #总页数
    total_count = query.count()
    total_page = math.ceil(total_count/per_page)
    if page < 1:
        items = []
    else:
        items = query.limit(per_page).offset((page-1) * per_page).all()
    current_page = page
    pagination = {'total_page': total_page, 'current_page': current_page,
                  'items': items,'count':len(items)}
    return pagination

def code_formate(code, count=4):
    code = str(code)
    code_len = len(code)
    if code_len > count or not code.isdigit():
        raise Exception('code not allowed')
    return (count-len(code)) * '0' + str(code)

#小写金额转换大写
def to_china_amount(nin):
    try:
        cs =('零','壹','贰','叁','肆','伍','陆','柒','捌','玖','◇',
            '分','角','圆','拾','佰','仟','万','拾','佰','仟','亿',
            '拾','佰','仟','万')

        st = ''
        st1=''
        s ='%0.2f'%nin
        sln =len(s)
        if sln>15:
            return None
        fg = (nin<1)
        for i in range(0, sln-3):
            ns = ord(s[sln-i-4]) - ord('0')
            st=IIf((ns==0) and (fg or (i==8) or (i==4) or (i==0)),'',cs[ns]) \
                + IIf((ns==0)and((i!=8)and(i!=4)and(i!=0) or fg and(i==0)),'', cs[i+13]) + st
        fg = (ns==0)
        fg = False
        for i in [1,2]:
            ns = ord(s[sln-i]) - ord('0')
            st1 = IIf((ns==0) and ((i==1)or(i==2) and (fg or (nin<1))), '', cs[ns]) + \
                    IIf((ns>0),cs[i+10], 
                    IIf((i==2) or fg, '', '整'))+ st1
            fg = (ns==0)
        st.replace('亿万','万')
        return IIf( nin==0, '零', st + st1)
    except:
        return '零圆'

def IIf(b,s1,s2):
    if b:
        return s1
    else:
        return s2

#获取每个月份的天数
def get_month_days(year,month ):
    day = 31                #定义每月最多的天数
    while day:
        try:
            time.strptime( '%s-%s-%d'%( year, month, day ), '%Y-%m-%d' ) #尝试将这个月最大的天数的字符串进行转化
            return day      #成功时返回得就是这个月的天数
        except:
            day -= 1        #否则将天数减1继续尝试转化, 直到成功为止