# !/usr/bin python3
# -*- coding: utf-8 -*-
"""
 @file:untils.py
 @time:2021/06/16/16:38
 @detail:
 """
from service import es_logger


def compare_time(current_time_stamp, time_limit, last_time_stamp):
    """
    return True:当前距离上次采集时间超过指定间隔时间
    return False:当前距离上次采集时间未超过指定间隔时间
    :param current_time_stamp:
    :param time_limit:
    :param last_time_stamp:
    :return:
    """
    if current_time_stamp - last_time_stamp > time_limit:
        return True
    else:
        return False


def save_db(collection, item):
    try:
        collection.insert_one(item)
    except Exception as e:
        # es_logger.error(e)
        pass


def update_db(collection, condition, item):
    try:
        collection.update(condition, {"$set": item}, True, True)
    except Exception as e:
        es_logger.error(e)


def get_data(collection, query=None, limit=20):
    """
    从指定集合获取数据(查询用)
    :param query:
    :param collection:
    :param limit: 获取数据量大小
    :return:
    """
    # query["_id"] = {"$gte": position}
    if query is None:
        query = {}
    return list(collection.find(query).sort([("_id", 1)]).limit(limit))
