# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2020/4/10 11:11
 @IDE  : PyCharm
 """

from pymongo import MongoClient

mongo = MongoClient("mongodb://127.0.0.1:27017/KF")
dest_db = mongo.get_database()
collection = dest_db.get_collection("jdkf")
li = collection.find({})

new_set = set()
for info in li:
    chat_time = info['chat_time']
    shop_name = info['shop_name']
    elements = info['element']['chatLogMessageList']
    print(elements[0]['customer'])
#     for element in elements:
#         customer = element['customer']
#         sid = hashlib.md5((chat_time + customer + shop_name).encode('utf-8')).hexdigest()
#         new_set.add(sid)
# print(new_set, len(new_set))
