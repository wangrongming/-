import datetime
from importlib import import_module
from pathlib import Path

from absl import app, flags

from service import es_logger

flags.DEFINE_integer("worker", 1, help="爬虫节点运行的线程数")
flags.DEFINE_string("plat", "list|detail|comment|reply", help="eg: list|detail|comment|reply 或 list")
flags.DEFINE_integer("max_page", 10, help="最大采集页数")
flags.DEFINE_string("mongo", "mongodb://root:Bqi7io41KUIx@192.168.21.22:27017", help="mongo数据库")
flags.DEFINE_integer("interval", 14400, help="采集时间间隔（秒）")
flags.DEFINE_string("start_time", "", help="采集新闻开始时间：默认当前时间-时间间隔  格式:2021-06-15 00:00:00")
flags.DEFINE_string("end_time", "", help="采集新闻开始时间：默认当前时间-时间间隔  格式:2021-06-15 00:00:00")


def main(argv):
    if not flags.FLAGS.start_time:
        end_time = datetime.datetime.now()
        end_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        start_time = end_time - datetime.timedelta(seconds=flags.FLAGS.interval)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

    else:
        start_time_str = flags.FLAGS.start_time
        end_time_str = flags.FLAGS.end_time
    es_logger.info(f"当前采集内容包含：{flags.FLAGS.plat}")
    es_logger.init_logger("dataheap_crawler", Path.cwd().absolute() / "logs/dataheap_crawler.log")

    yt = import_module('spider.people')
    yt.main(start_time_str, end_time_str)


if __name__ == '__main__':
    app.run(main)
