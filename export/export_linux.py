# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/12/3 14:10
 @Auth : 明明
 @IDE  : PyCharm
 """
import platform
import re

import pymongo
from openpyxl import Workbook


def export():
    if 'Win' in platform.system():
        client = pymongo.MongoClient('127.0.0.1', 27017)
    else:
        client = pymongo.MongoClient('10.1.6.173', 28018)

    db = client["KF"]
    collection = db["tmkf"]

    wb = Workbook()
    ws = wb.active
    for info in collection.find({"chat_time": re.compile('2019-11-04')}).sort("waiter", 1):
        info.pop("_id")
        cols_val = []
        for k in info:
            cols_val.append(repr(info[k]))
        ws.append(cols_val)  # 写值
    wb.save("20191104_tm_kf.xlsx")
    print("存储完毕")


if __name__ == '__main__':
    export()
