#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def init_logger(module, file_name: Path, name="es_logger"):
    """
    json 格式输出日志到文件，由 filebeat 同步到 elastisearch 做分析、追踪
    :param module: 指定应用
    :param file_name: 日志文件名称
    :param name: 日志句柄
    :return:
    """
    if not file_name.parent.exists():
        file_name.parent.mkdir(parents=True)

    log_fmt = '{"created_at":%(created)d,"file":"%(filename)s","line":%(lineno)s,' \
              f'"module":"{module}","level":"%(levelname)s","message":"%(message)s","extra":%(extra)s}}'
    formatter = logging.Formatter(log_fmt)
    log_file_handler = RotatingFileHandler(filename=file_name,
                                           maxBytes=209715200, backupCount=10,
                                           encoding='utf-8')
    log_file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger(name).addHandler(log_file_handler)


def info(message, extra=None, name="es_logger"):
    if not extra:
        extra = {}
    logging.getLogger(name).info(message, extra={"extra": json.dumps(extra, ensure_ascii=False)})


def debug(message, extra=None, name="es_logger"):
    if not extra:
        extra = {}
    logging.getLogger(name).debug(message, extra={"extra": json.dumps(extra, ensure_ascii=False)})


def error(message, extra=None, name="es_logger"):
    if not extra:
        extra = {}
    logging.getLogger(name).error(message, extra={"extra": json.dumps(extra, ensure_ascii=False)})


def warning(message, extra=None, name="es_logger"):
    if not extra:
        extra = {}
    logging.getLogger(name).warning(message, extra={"extra": json.dumps(extra, ensure_ascii=False)})


def exception(message, extra=None, name="es_logger"):
    if not extra:
        extra = {}
    logging.getLogger(name).exception(message, extra={"extra": json.dumps(extra, ensure_ascii=False)})
