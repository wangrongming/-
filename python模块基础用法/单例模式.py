# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2020/1/20 12:09
 @Auth : 明明
 @IDE  : PyCharm
 """

import threading


class Singleton(object):
    _instance_lock = threading.Lock()  # 保证线程安全

    def __init__(self):
        self.name = 1

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance


obj1 = Singleton()
obj2 = Singleton()
print(obj1, obj1.name)
print(obj2, obj2.name)
