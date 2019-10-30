# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/10/29 14:25
 @Auth : 明明
 @IDE  : PyCharm
 """

import logging
# logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#                     level=logging.INFO)
# logger = logging.getLogger(__name__)
#
#
# logger.debug('debug 信息')
# logger.info('info 信息')
# logger.warning('warning 信息')
# logger.error('error 信息')
# logger.critical('critial 信息')


import sys

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    # filename='new.log',
                    # filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    stream=sys.stdout
                    #日志格式
                    )
logger = logging.getLogger(__name__)


logger.debug('debug 信息')
logger.info('info 信息')
logger.warning('warning 信息')
logger.error('error 信息')
logger.critical('critial 信息')