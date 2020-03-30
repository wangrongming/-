# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2020/3/10 10:35
 @IDE  : PyCharm
 """

from absl import app
from absl import flags

# 设置参数，第一个是参数名称，第二个是参数默认值，无默认值可取None，第三个是参数解释
flags.DEFINE_string('str_1', 'hello', 'Input a string.')
flags.DEFINE_string('str_2', 'world', 'Input a string.')

flags.DEFINE_integer('num_1', 1212, 'Input a integer.')
flags.DEFINE_integer('num_2', 1313, 'Input a integer.')


def main(argv=()):
    del argv
    print(flags.FLAGS.str_1)
    print(flags.FLAGS.str_2)
    print(flags.FLAGS.num_1)
    print(flags.FLAGS.num_2)


# 如果当前是从其它模块调用的该模块程序，则不会运行main函数！
# 而如果就是直接运行的该模块程序，则会运行main函数。
if __name__ == '__main__':
    app.run(main)
