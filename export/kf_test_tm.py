# -*- coding: utf-8 -*-
import platform
import re

import pymongo
from openpyxl import Workbook

if 'Win' in platform.system():
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None

    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017

    kafka_host = "192.168.0.158:9092"

else:
    REDIS_HOST = '10.1.6.8'
    REDIS_PORT = 6379
    REDIS_PASSWORD = "kaVd9*F(Ax#q"

    MONGO_HOST = '10.1.6.173'
    MONGO_PORT = 28018

    kafka_host = ['10.1.6.25:9092', '10.1.6.24:9092']

client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client["KF"]
set_collection = db["tmkf"]


def change():
    print("insert_len", set_collection.find({"chatTime": re.compile('2019-11-27')}).count())
    for info in set_collection.find({"chatTime": re.compile('2019-11-27')}):
        if "shopName" in info.keys():
            item = {
                "shop_name": info['shopName'],
                "username": info['username'],
                "from_url": info['fromUrl'],
                "waiter": info['waiter'],
                "customer": info['customer'],
                "source_id": info['sourceId'],
                "chat_time": info['chatTime'],
                "sid": info['sid'],
                "chat_info": info['chatInfo'],
                "grap_time": info['grapTime'],
                "insert_timestamp": info['insertTimestamp'],
                "_class": info['_class']
            }
        else:
            info.pop("_id")
            item = info
        set_collection.insert_one(item)

    del_res = set_collection.delete_many({"chatTime": re.compile('2019-11-27')})
    print("del_res", del_res)


def query_info():
    name_li = [name for name in set_collection.distinct("customer", {"waiter": {"$ne": "cntaobaooppo官方旗舰店:服务助手"}})]
    for new_name in set_collection.distinct("customer"):
        if new_name not in name_li:
            print(new_name)


def query_content():
    li_all = []
    li_contains = []
    li_single = []

    for info in set_collection.find(
            {"waiter": {"$ne": "cntaobaooppo官方旗舰店:服务助手"}, "chat_time": re.compile("2019-11-05")}):
        customer = re.sub("cntaobao", "", info['customer'])
        chat_info = info['chat_info']
        li_all.append(customer)
        if customer not in chat_info:
            li_single.append(customer)
        else:
            li_contains.append(customer)

    li_contains = list(set(li_contains))
    li_single = list(set(li_single))
    li_all = list(set(li_all))
    print("len(li_single)", len(li_single))
    print(li_single)
    print("len(li_contains)", len(li_contains))
    print(li_contains)
    print("len(li_all)", len(li_all))
    print(li_all)


def export_content():
    wb = Workbook()
    ws = wb.active
    li_contains = []
    for info in set_collection.find(
            {"waiter": {"$ne": "cntaobaooppo官方旗舰店:服务助手"}, "chat_time": re.compile("2019-11-05")}):
        customer = re.sub("cntaobao", "", info['customer'])
        chat_info = info['chat_info']
        if customer not in chat_info:
            continue
        if customer not in li_contains:
            li_contains.append(customer)
            info.pop("_id")
            cols_val = []
            for k in info:
                cols_val.append(repr(info[k]))
            ws.append(cols_val)  # 写值
    wb.save("20191104_tm_kf.xlsx")


if __name__ == '__main__':
    # change()
    # query_info()
    query_content()
    # export_content()
