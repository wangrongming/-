#!/usr/bin/python
import datetime

# 使用datetime模块来获取当前的日期和时间
# 参数如下：
import random
import time

cur = datetime.datetime.now()
print(cur, cur.isoformat())
print(cur.year)
print(cur.month)
print(cur.day)
print(cur.hour)
print(cur.minute)
print(cur.second)

# 当前时间前一天
d = datetime.datetime.now()
one_day = datetime.timedelta(days=1)
yesterday = d - one_day
print(yesterday)

# 当前时间标准化
info = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(info)

# 字符转时间
str_time = datetime.datetime.strptime("2019-10-11 11:26:34", '%Y-%m-%d %H:%M:%S')
print(str_time)
print(int(str_time.timestamp()))

# 时间戳转日期 方案一
d = datetime.datetime.fromtimestamp(1573186027)
str1 = d.strftime("%Y-%m-%d %H:%M:%S")
print("str1", str1)

# 时间戳转日期 方案二
st = time.localtime(int(1573186027))
publish_time = time.strftime('%Y-%m-%d', st)

if __name__ == '__main__':
    pass

# 带t时间
import dateutil.parser


def getDateTimeFromISO8601String(s):
    d = dateutil.parser.parse(s)
    return d


if __name__ == '__main__':
    a = getDateTimeFromISO8601String('2018-01-01T00:00:00')
    print(a)
    # 4542626659930211
    # 5769657468981557
    # 7991412311012391
    print(str(random.random())[2:])
