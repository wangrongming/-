import logging.handlers
import os
import sys
from logging.handlers import RotatingFileHandler


def init_logger():
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # 日志输出到文件
    formatter_str_file = '{"createdAt":%(created)f,"spider_name":"%(name)s","type":"%(type)s","level":"%(levelname)s",' \
                         '"message":"%(message)s","code":%(code)s,"step":"spider","get_sku_time":%(get_sku_time)f,' \
                         '"collect_time":%(collect_time)f,"deduplication_time":%(deduplication_time)f,' \
                         '"save_time":%(save_time)f,"api":"%(api)s",' \
                         '"api_url":"%(api_url)s","cost":%(cost)s}'
    formatter_file = logging.Formatter(formatter_str_file)

    file_handler = RotatingFileHandler(filename="logs/cookie_factory.log", maxBytes=200 * 1024 * 1024,
                                       backupCount=10,
                                       encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter_file)

    # 日志输出到终端
    formatter_str_console = '%(asctime)s %(levelname)s %(pathname)s %(message)s'
    formatter_console = logging.Formatter(formatter_str_console)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter_console)

    # # 全局设置日志
    logging.root.addHandler(file_handler)
    logging.root.addHandler(console_handler)
