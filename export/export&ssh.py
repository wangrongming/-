# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/12/3 14:10
 @Auth : 明明
 @IDE  : PyCharm
 """
import re

import pymongo
from openpyxl import Workbook
from sshtunnel import SSHTunnelForwarder  # ssh连接库

server = SSHTunnelForwarder(
    ssh_address_or_host=('115.159.127.155', 22),  # ssh地址
    ssh_username='root',  # ssh连接的用户名
    ssh_password='TLkxPI6BzgJcZA97',  # ssh连接的用户名
    remote_bind_address=('10.1.6.173', 28018),
    local_bind_address=('127.0.0.1', 10022))

with server:
    client = pymongo.MongoClient('127.0.0.1', 10022)
    db = client["KF"]
    collection = db["tmkf"]
    res = collection.find({"chat_time": re.compile('2019-11-04')}).sort("customer")

    wb = Workbook()
    ws = wb.active
    for info in res:  # .sort({"brand", "keyword", "type", "from_url"})
        info.pop("_id")
        cols_val = []
        for k in info:
            cols_val.append(repr(info[k]))
        ws.append(cols_val)  # 写值
    wb.save("20191104_tm_kf.xlsx")
    print("存储完毕")

if __name__ == '__main__':
    pass
