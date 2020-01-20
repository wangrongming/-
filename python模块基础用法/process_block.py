# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2020/1/20 16:26
 @Auth : 明明
 @IDE  : PyCharm
 """
import multiprocessing
from multiprocessing.pool import Pool


def task(i):
    print("多进程 当前传入参数为{}".format(i))


def process_one():
    p_li = []
    for i in range(1, 6):
        process = multiprocessing.Process(target=task, args=(i,))
        process.start()
        p_li.append(process)

    for info in p_li:
        info.join()
        info.close()


def process_two():
    # multiprocessing
    pool = Pool(3)
    for i in range(1, 6):
        pool.apply_async(task, (i,))  # 非阻塞 有返回值
        pool.apply(task, (i,))  # 阻塞 无返回值

    msg_li = [1, 2, 3, 4, 5]
    pool.map(task, msg_li)  # 阻塞 无返回值
    pool.imap(task, msg_li)  # 非阻塞 无返回值

    pool.close()
    pool.join()


if __name__ == '__main__':
    process_one()
