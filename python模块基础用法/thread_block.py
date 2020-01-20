# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2020/1/20 16:26
 @Auth : 明明
 @IDE  : PyCharm
 """
# 多线程
import threading
from multiprocessing import dummy


def task(i):
    print("当前传入参数为{}".format(i))


def thread_one():
    li = []

    for i in range(5):
        t = threading.Thread(target=task, args=(i,))
        li.append(t)
        t.start()
        t.join()

    for t in li:
        t.join()


def thread_two():
    """
    1 非阻塞方法
        multiprocessing.dummy.Pool.apply_async() 和 multiprocessing.dummy.Pool.imap()
        线程并发执行

    2 阻塞方法
        multiprocessing.dummy.Pool.apply()和 multiprocessing.dummy.Pool.map()
        线程顺序执行
    """
    pool = dummy.Pool(4)
    chat_arg_list = [1, 2, 3, 4, 5]

    for i in range(1, 6):
        pool.apply_async(task, args=(i,))  # 非阻塞 有返回值
        pool.apply(task, args=(i,))  # 阻塞 无返回值

    # 非阻塞
    pool.imap(task, chat_arg_list)  # 非阻塞 无返回值
    pool.map(task, chat_arg_list)  # 阻塞 无返回值

    pool.close()
    pool.join()


if __name__ == '__main__':
    thread_two()
