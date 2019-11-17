# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/10/28 14:28
 @Auth : 明明
 @IDE  : PyCharm
 """
# -*- coding: utf-8 -*
import json
import xlwt
import os
import sys
import pymongo
from setting import MONGO_HOST, MONGO_PORT, REDIS_HOST, REDIS_PORT

client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)


# def readjson():
#     db = client["OTHERS"]
#     collection = db["zhihu_answer"]
#     info_li = []
#     info = collection.find({})
#     j = 0
#     for i in info:
#         j += 1
#         if j > 2000:
#             break
#         info_li.append(i)
#     return info_li

def readjson():
    db = client["Tool"]
    collection = db["tmpd_haier"]
    info_li = []
    info = collection.find({})
    j = 0
    for i in info:
        j += 1
        if j > 2000:
            break
        info_li.append(i)
    return info_li


from openpyxl import Workbook
wb = Workbook()
ws = wb.active


def json2excel(excfile="haier.xlsx"):
    db = client["Tool"]
    collection = db["tmpd_haier"]
    info = collection.find({})
    for jsdata in info:
        jsdata.pop("_id")
        cols_val = []
        for k in jsdata:
            cols_val.append(jsdata[k])
        ws.append(cols_val)  # 写值
    wb.save(excfile)


if __name__ == '__main__':
    json2excel()
