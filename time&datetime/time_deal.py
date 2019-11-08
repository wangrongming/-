#!/usr/bin/python
import datetime

# 使用datetime模块来获取当前的日期和时间
# 参数如下：
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
import time


def deal_time(st_time="2019-11-05 20:20"):
    str_time = datetime.datetime.strptime(st_time, '%Y-%m-%d %H:%M:%S')
    print(str_time)
    print(int(time.time() - int(str_time.timestamp())))


if __name__ == '__main__':
    deal_time()