# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/10/28 14:08
 @Auth : 明明
 @IDE  : PyCharm
 """
import platform

if 'Win' in platform.system():
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
else:
    # 内网mongodb—redis库
    MONGO_HOST = '10.1.6.16'
    MONGO_PORT = 28018

    REDIS_HOST = '10.1.4.81'
    REDIS_PORT = 6379