# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2020/1/20 12:09
 @Auth : 明明
 @IDE  : PyCharm
 """

import threading


# 这里需要注意的是，如果__new__函数返回一个已经存在的实例（不论是哪个类的），__init__不会被调用。如下面代码所示

class Singleton(object):
    _instance_lock = threading.Lock()  # 保证线程安全

    def __init__(self):
        print("__init__")

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance


obj1 = Singleton()
obj2 = Singleton()
print(obj1)
print(obj2)
