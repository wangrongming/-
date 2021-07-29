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
# li = collection.find({})

# new_set = set()
# for info in li:
#     chat_time = info['chat_time']
#     shop_name = info['shop_name']
#     elements = info['element']['chatLogMessageList']
#     print(elements[0]['customer'])

#     for element in elements:
#         customer = element['customer']
#         sid = hashlib.md5((chat_time + customer + shop_name).encode('utf-8')).hexdigest()
#         new_set.add(sid)
# print(new_set, len(new_set))


# collection.insert_one({"V.Constantin/江诗丹顿品牌": "Égérie伊灵女神系列"})
# res = collection.insert({"V.Constantin/江诗丹顿品牌": "Égérie伊灵女神系列"}, check_keys=False)
# res = collection.insert([{"V.Constantin/江诗丹顿品牌": "Égérie伊灵女神系列"}], check_keys=False)
# print(res)

li = [{"V.Constantin/江诗丹顿品牌": "Égérie伊灵女神系列"}]


def dict_data_pre_process(data_):
    """
    dict 集合数据预处理
    :param data_:
    :return:
    """
    if isinstance(data_, dict):
        data = data_
        for _k in data.keys():
            data[_k.replace('.', '_')] = data.pop(_k)
            try:
                dict_data_pre_process(data[_k])
            except:
                pass
    elif isinstance(data_, list):
        for data in data_:
            for _k in data.keys():
                data[_k.replace('.', '_')] = data.pop(_k)
                try:
                    dict_data_pre_process(data[_k])
                except:
                    pass


dict_data_pre_process(li)
print(li)

# 指定用户名密码验证建立mongo
# ./bin/mongod --dbpath /mnt/mongodb/data --logpath /mnt/mongodb/mongod.log --bind_ip 0.0.0.0 --port=28018 --auth --logappend --fork
# ./bin/mongod --dbpath /mnt/mongodb/data --logpath /mnt/mongodb/mongod.log --bind_ip 0.0.0.0 --port=28018 --auth --logappend --fork
# ./bin/mongod --dbpath /mnt/mongodb/data --logpath /mnt/mongodb/mongod.log --bind_ip 0.0.0.0 --port=28018 --logappend --fork
# ./bin/mongo --host 127.0.0.1 --port 28018  (当前服务器内网ip)
# 然后创建一个用户 devUser, 密码是 P@55w0rd
# use admin
# db.createUser({
#     user:"devUser",
#     pwd:"Pa55word",
#     roles:[{
#         role:"root",
#         db:"admin"
#     }]
# })
# db.auth("devUser", "Pa55word")
# db.changeUserPassword("devUser","Pa55word");
# ip: 112.74.191.185
# 端口：28018
# db:admin
# user: devUser
# pwd: Pa55word
