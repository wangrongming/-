# !/usr/bin python3
# -*- coding: utf-8 -*-
"""
 @file:spider.py
 @detail:
 """
import datetime
import json
import logging
import time
import traceback
from multiprocessing import dummy

import requests
from absl import flags
from bson import ObjectId
from lxml import etree

from service import es_logger
from service.service import keyword_col, list_col, position_col, content_col
from service.untils import save_db, get_data, update_db


def get_list(dt, start_time, end_time, page=1):
    start_time = int(datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').timestamp()) * 1000
    end_time = int(datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').timestamp()) * 1000
    keyword = dt['keyword']
    if not keyword:
        return
    url = "http://search.people.cn/api-search/elasticSearch/search"
    headers = {
        "Host": "search.people.cn",
        "Proxy-Connection": "keep-alive",
        "Content-Length": "133",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.77 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://search.people.cn",
        "Referer": f"http://search.people.cn",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "sso_c=0; sfr=1",
    }
    data = {
        "key": keyword,
        "page": page,
        "limit": 10,
        "hasTitle": True,
        "hasContent": True,
        "isFuzzy": False,
        "type": 1,
        "sortType": 0,
        "startTime": start_time,
        "endTime": end_time,
    }
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    li = res.json()['data']['records']
    es_logger.info(f"人民网 采集关键词：{keyword} 第{page}页")
    for _ in li:
        item = {
            "keyword": keyword,
            "website_url": "http://www.people.com.cn/",
            "website_name": "人民网",
            "news_id": _.get("id", ""),
            "news_url": _.get("url", ""),  # 新闻在人民网链接
            "news_source": _.get("originalName", ""),  # 新闻来源：人民网-人民日报，强国论坛
            "news_source_url": _.get("originUrl", ""),  # 新闻来源原始链接
            "news_type": _.get("belongsName", ""),  # 类别（社会，科技）
            "title": _.get("title", "").strip(),  # 标题
            "publish_time": _.get("displayTime", ""),  # 新闻发布时间
            "author": _.get("author", "").strip(),  # 发布者
            "editor": _.get("editor", "").strip(),  # 编辑
            "view_count": "",  # 浏览量
            "tags_count": "",  # 点赞量
            "comment_count": "",  # 评论量
            "content": "",
            "insert_timestamp": int(time.time() * 1000)  # 数据插入时间
        }
        save_db(list_col, item)

    if page == 1:
        total_page = res.json()['data']['pages']
        return total_page


def get_detail(dt):
    try:
        url = dt['news_url']
        if "people" not in url:
            return
        headers = {
            "Proxy-Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        res = requests.get(url=url, headers=headers)
        selector = None
        try:
            selector = etree.HTML(res.content.decode("gbk"))
        except Exception as e:
            pass
            try:
                selector = etree.HTML(res.content.decode("utf-8"))
            except Exception as e:
                pass

        if selector is None:
            return

        editor_one = selector.xpath("//*[@class='edit cf']")
        editor_two = selector.xpath("//*[contains(text(),'责编')]")
        editor_three = selector.xpath("//*[@class='edit clearfix']")
        if editor_one:
            editor = editor_one[0].xpath("string(.)").strip()
            dt['editor'] = editor
        elif editor_two:
            editor = editor_two[0].xpath("string(.)").strip()
            dt['editor'] = editor
        elif editor_three:
            editor = editor_three[0].xpath("string(.)").strip()
            dt['editor'] = editor

        content = ""
        box_con = selector.xpath("//div[@class='box_con']")
        show_text = selector.xpath("//div[@class='show_text']")
        col = selector.xpath("//div[@class='col col-1 fl']")
        two = selector.xpath("//div[@class='w1200 rm_txt cf']")
        three = selector.xpath("//div[@class='WB_detail']")
        four = selector.xpath("//div[@class='content clear clearfix']")
        five = selector.xpath("//div[@class='col col-1']")
        if box_con:
            content = box_con[0].xpath("string(.)").strip()
        elif show_text:
            content = show_text[0].xpath("string(.)").strip()
        elif col:
            content = col[0].xpath("string(.)").strip()
        elif two:
            content = two[0].xpath("string(.)").strip()
        elif three:
            content = three[0].xpath("string(.)").strip()
        elif four:
            content = four[0].xpath("string(.)").strip()
        elif five:
            content = five[0].xpath("string(.)").strip()
        else:
            # es_logger.error("其他selector:{}".format(url))
            pass
        if content:
            dt.pop("_id", None)
            dt['insert_timestamp'] = int(time.time() * 1000)
            dt['content'] = content
            save_db(content_col, dt)
    except Exception as e:
        es_logger.info(f"{traceback.format_exc()}{e}")


def main_list(start_time, end_time):
    """
    列表页循环采集
    :return:
    """
    # last_time_stamp = 0
    while True:
        max_page = flags.FLAGS.max_page
        # interval = flags.FLAGS.interval

        # # 每4个小时遍历一次，查看当前采集时间是否满足采集要求
        # current_time_stamp = int(time.time())
        # if not compare_time(current_time_stamp, interval, last_time_stamp):
        #     es_logger.info(
        #         f"当前时间{current_time_stamp} 上一次采集时间{last_time_stamp} 采集间隔小于 指定时间间隔：{interval / 3600}h 休眠60s ")
        #     time.sleep(60)
        #     continue
        # last_time_stamp = current_time_stamp

        # 采集
        try:
            for _ in keyword_col.find():
                total_page = get_list(_, start_time, end_time, page=1)
                if total_page < max_page:
                    max_page = total_page
                for i in range(2, max_page + 1):
                    get_list(_, start_time, end_time, page=i)
            break
        except Exception as e:
            es_logger.info(f"{traceback.format_exc()}{e}")


def main_detail():
    # 详情页查询位置:有新增则采集，无新增不采集
    # 重置位置:
    while True:
        try:
            position = get_data(position_col, query={}, limit=1)
            query = {}
            if position:
                query = {"_id": {"$gt": ObjectId(position[0]['list_position'])}}
            elements = get_data(list_col, query=query)
            if len(elements) == 0:
                es_logger.info("详情页 采集完成，程序退出")
                break
            start_position = elements[0]["_id"]
            end_position = elements[-1]["_id"]
            es_logger.info(
                f"开始采集 详情页内容 start_position：{start_position};end_position:{end_position}; len:{len(elements)}")
            pool = dummy.Pool(flags.FLAGS.worker)
            pool.map(get_detail, elements)
            pool.close()
            pool.join()

            condition = {"collection": "list_position"}
            item = {"list_position": end_position}
            update_db(position_col, condition, item)

            time.sleep(1)
        except Exception as e:
            logging.error(f"{traceback.format_exc()} {e}")


def main(start_time, end_time):
    plat = flags.FLAGS.plat  # list|detail|comment|reply
    # 1 遍历关键词：进行列表页采集
    if "list" in plat:
        main_list(start_time, end_time)
    # 2 读取mongo列表表：进行详情页采集 多线程
    if "detail" in plat:
        main_detail()
    # 3 读取mongo详情表：进行评论采集 多线程
    # 4 读取mongo评论表：进行评论回复采集 多线程


if __name__ == '__main__':
    main("", "")
    # get_list({"keyword": "时代"})
