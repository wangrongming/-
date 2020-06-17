import logging.handlers
import os
import sys
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def init_logger():
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # 日志输出到文件
    formatter_str_file = '%(asctime)s    %(levelname)s   %(appname)s:  %(message)s'

    formatter_file = logging.Formatter(formatter_str_file)

    file_handler = RotatingFileHandler(filename="logs/cookie_factory.log", maxBytes=200 * 1024 * 1024,
                                       backupCount=10,
                                       encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter_file)

    # 日志输出到终端
    formatter_str_console = '%(asctime)s    %(levelname)s   %(appname)s:  %(message)s'
    formatter_console = logging.Formatter(formatter_str_console)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter_console)

    # # 全局设置日志
    # logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger('eslogger').addHandler(file_handler)
    logging.getLogger('eslogger').addHandler(console_handler)


if __name__ == '__main__':
    init_logger()
    logger = logging.getLogger('eslogger')
    # logger.setLevel(logging.INFO)
    logger.info("ceshi", extra={'appname': '自定义变量'})
