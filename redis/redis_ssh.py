#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/19 18:34
# @Author  : Hing Lee
# @Software: PyCharm
import time

from sshtunnel import SSHTunnelForwarder  # ssh连接库
import redis  # redis模块

server = SSHTunnelForwarder(
    ssh_address_or_host=('115.159.127.155', 22),  # ssh地址
    ssh_username='root',  # ssh连接的用户名
    ssh_password='TLkxPI6BzgJcZA97',  # ssh连接的用户名
    remote_bind_address=('10.1.6.8', 6379),
    local_bind_address=('127.0.0.1', 10022))

with server:
    start_time = time.time()
    r = redis.Redis(host='127.0.0.1', port=10022, db=3, password="kaVd9*F(Ax#q", decode_responses=True)  # decode_responses: 解码
    print(r.lrange('zhihu_search_full:question_id', 0, -1))
    end_time = time.time()
    during = end_time - start_time
    print(during)
    # print(r.keys('*'))