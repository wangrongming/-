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
    collection = db["tmpd"]
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

cols = []


def json2excel(excfile):
    all = readjson()
    a = 1
    for k in all[0].keys():
        cols.append(k)
    ws.append(cols)  # 标题

    for jsdata in all:
        cols_val = []
        for k in jsdata:
            cols_val.append(repr(jsdata[k]))
        ws.append(cols_val)  # 写值

    wb.save(excfile)


if __name__ == '__main__':
    excfile = "baicaowei.xlsx"
    json2excel(excfile)
