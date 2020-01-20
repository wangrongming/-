# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/10/29 14:25
 @Auth : 明明
 @IDE  : PyCharm
 """
import logging
import os
from logging.handlers import RotatingFileHandler

if not os.path.exists("logs"):
    os.mkdir("logs")

# 改动日志格式，修改相应的 elasticsearch 模板 http://wiki.skieer.com/pages/viewpage.action?pageId=27344191
format = '{"created_at":%(created)f,"file":"%(filename)s","line":%(lineno)s,' \
         '"app":"task_dispatcher","level":"%(levelname)s","message":"%(message)s"}'
formatter = logging.Formatter(format)
log_file_handler = RotatingFileHandler(filename="logs/task-dispatcher.log", maxBytes=209715200, backupCount=10,
                                       encoding='utf-8')  # 根据文件大小最多切分为10条日志
log_file_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger("eslogger").addHandler(log_file_handler)

logger = logging.getLogger("eslogger")
logger.info("ni hao")
