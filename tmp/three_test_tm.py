# -*- coding: utf-8 -*-
import platform
import re

import pymongo

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


if __name__ == '__main__':
    change()
