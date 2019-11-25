# coding:utf-8
import datetime
import logging
import platform
import random
import re
import sys
import time
import traceback
from hashlib import sha1
from urllib.parse import urljoin

import pymongo
import requests
import tenacity
from kafka_template import KafkaTemplate
from lxml import etree
from tenacity import stop_after_attempt, wait_fixed

import redis
from setting import REDIS_PORT, REDIS_HOST, REDIS_PASSWORD, redis_db_hw, redis_posting_hw_part, redis_posting_hw_full, \
    MONGO_HOST, MONGO_PORT, kafka_host

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger(__name__)
if 'Win' in platform.system():
    pass
else:
    pass
cookies_login = {}
proxies = {}
element_unique = None


def get_proxy(retry_state):
    global proxies
    while True:
        url1 = 'http://proxy.yuntingai.com/proxy/getProxy/14'
        try:
            res = requests.get(url1, timeout=3)
            if res.status_code != 200:
                continue
            proxy_info = res.json()
            if proxy_info.get('trueIp'):
                if proxy_info['type'] == 'http':
                    proxy_info['type'] = 'http'
                else:
                    proxy_info['type'] = 'socks5'
                type_info = proxy_info['type']
                name = proxy_info['name']
                password = proxy_info['password']
                host = proxy_info['host']
                port = proxy_info['port']
                proxies = {
                    'https': "{}://{}:{}@{}:{}".format(type_info, name, password, host, port),
                    'http': "{}://{}:{}@{}:{}".format(type_info, name, password, host, port),
                }
                break
            else:
                time.sleep(2)
                continue
        except Exception:
            logger.info(traceback.format_exc())
            time.sleep(3)


class HUAWEI(object):
    """
    花粉版块 帖子采集
    """

    def __init__(self, spider_type):
        self.spider_type = spider_type.lower()
        self.redis_cli = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=redis_db_hw)
        if self.spider_type == "full":
            self.redis_posting = redis_posting_hw_full
        else:
            self.redis_posting = redis_posting_hw_part
        self.headers = {
            'Connection': "keep-alive",
            'Cache-Control': "max-age=0",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebK"
                          "it/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            'Sec-Fetch-Mode': "navigate",
            'Sec-Fetch-User': "?1",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9"
                      ",image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Sec-Fetch-Site': "none",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'cache-control': "no-cache",
        }
        self.client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client["CEM"]
        self.collection = self.db["huawei"]
        self.kafka_template = KafkaTemplate(kafka_host)

    @tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1))
    def get_replies_full(self, page, item_before):
        """
        全量 最新发帖
        :return:
        """
        url = "https://club.huawei.com/viewthreaduni-{}-filter-author-orderby-dateline-page-1-{}.html".format(
            item_before['posting_id'], page)
        response = requests.request("GET", url, headers=self.headers)
        html = response.text
        if "华为帐号-登录" in html:
            logger.info("当前帖子需要登录后爬取 {}".format(url))  # TODO 暂时不作处理
            return
        selector = etree.HTML(html)
        post_list = selector.xpath("//*[@id='postlist']/div")
        for post_info in post_list:
            self.parse_element(post_info, item_before, url)

    @tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1))
    def get_user_info(self, url, params):
        response = requests.get(url, params=params, headers=self.headers)
        html = re.search(r"<root><!\[CDATA\[(.*?)]]></root>", response.text, re.S).group(1)
        selector = etree.HTML(html)
        u_name = selector.xpath('.//*[@class="cl cardclearfix"]/strong/a/text()')
        if u_name:
            u_name = u_name[0]
        else:
            u_name = ""

        user_logo = selector.xpath("//div[contains(@class,'card-avt')]/a/img/@src")
        if user_logo:
            user_logo = user_logo[0]
        else:
            user_logo = ""

        u_sign_day = selector.xpath('.//*[@class="cardclearfix"]/span/text()')
        if u_sign_day:
            u_sign_day = re.search(r"(\d+)", u_sign_day[0]).group(1)
        else:
            u_sign_day = ""

        u_club = selector.xpath('.//*[@class="cardclearfix"]/span/font/text()')
        if u_club:
            u_club = re.sub(r"\s|\n|\t", u_club[0])
        else:
            u_club = ""

        posting = selector.xpath('//*[@class="card-info"]/p/span/a/text()')
        if posting:
            posting = re.sub(r"\s|\n|\t", posting[0])
        else:
            posting = ""

        uid = selector.xpath("//span[contains(text(),'UID')]/text()")
        if uid:
            uid = re.sub(r"\s|\n|\t|UID|:", uid[0])
        else:
            uid = ""

        score = selector.xpath("//span[contains(text(),'积分')]/text()")
        if score:
            score = re.sub(r"\s|\n|\t|积分|:", score[0])
        else:
            score = ""

        online_time = selector.xpath("//span[contains(text(),'在线时间')]/text()")
        if online_time:
            online_time = re.sub(r"\s|\n|\t|在线时间|:", online_time[0])
        else:
            online_time = ""

        other_info = selector.xpath("//span[contains(text(),'在线时间')]/../span[2]")
        if other_info:
            other_info = re.sub(r"\s|\n|\t", other_info[0].xpath('string(.)'))
        else:
            other_info = ""

        item = {
            "u_name": u_name,
            "u_club": u_club,
            "u_sign_day": u_sign_day,
            "u_logo": user_logo,
            "posting": posting,
            "uid": uid,
            "score": score,
            "online_time": online_time,
            "other_info": other_info,
        }
        return item

    @tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1))
    def get_reply_ajax(self, url):
        response = requests.get(url, headers=self.headers)
        html = re.search(r"<root><!\[CDATA\[(.*?)]]></root>", response.text, re.S).group(1)
        selector = etree.HTML(html)
        return selector

    def parse_reply(self, comment_info, url, pid, item_before):
        # 判断是否有下一页
        comment_page = comment_info.xpath('.//a[text()="下一页"]/@onclick')
        if comment_page:
            url = re.search(r"ajaxget\(('forum.*?)'.*?", comment_page[0]).group(1)
            param = re.search(r"'(comment_\d+)'", comment_page[0]).group(1)
            url = url + "&" + param
            page_selector = self.get_reply_ajax(url)
            self.parse_reply(page_selector, url, pid, item_before)
        else:
            uid_url = comment_info.xpath('.//*[@class="psta vm"]/a/@href')
            if uid_url:
                uid_url = uid_url[0]
                user_final_url = urljoin(url, uid_url)
                params = {
                    "ajaxmenu": "1",
                    "inajax": "1",
                    "ajaxtarget": "ajaxid_{}_menu_content".format(random.random()),
                }
                user_info = self.get_user_info(user_final_url, params)
            else:
                user_info = {}
            user_name = comment_info.xpath('.//*[@class="psta vm"]/a[@class="xi2 xw1"]/text()')
            if user_name:
                user_name = user_name[0]
            else:
                user_name = ""
            user_logo = comment_info.xpath('.//*[@class="psta vm"]/a[starts-with(@class, "card")]/img/@src')
            if user_logo:
                user_logo = user_logo[0]
            else:
                user_logo = ""
            content = comment_info.xpath('.//*[@class="psti"]')
            if content:
                content = re.sub(r"\s|\n|\t|发表于.*", "", content[0].xpath('string(.)'))
            else:
                content = ""

            page_source = self.deal_page_source(comment_info)

            last_modify_time = comment_info.xpath('.//*[@class="psti"]/span/@title')
            if not last_modify_time:
                last_modify_time = comment_info.xpath('.//*[@class="psti"]/span/text()')
            if last_modify_time:
                str_posting_time = re.sub(r"\n|发表于\s+|\t", "", str(last_modify_time[0]))
                tmp_time = datetime.datetime.strptime(str_posting_time, '%Y-%m-%d %H:%M:%S')
                last_modify_time = int(tmp_time.timestamp()) * 1000
                last_modify_time_fmt = str_posting_time
            else:
                last_modify_time = ""
                last_modify_time_fmt = ""

            come_from = comment_info.xpath('.//*[@class="fmty"]/text()')
            if come_from:
                come_from = re.sub(r"\s|\n|\t", "", come_from[0])
            else:
                come_from = ""

            s = sha1()
            posting_title = item_before.get('posting_title')
            u_name = item_before.get('user_info').get('u_name')
            s.update((posting_title + u_name + content).encode())
            unique = s.hexdigest()

            reply = {
                "user_logo": user_logo,
                "user_name": user_name,
                "come_from": come_from,
                "last_modify_time": last_modify_time,
                "last_modify_time_fmt": last_modify_time_fmt,
                "content": content,
                "page_source": page_source,
                "favorite_number": "",
                "collection_number": "",
                "recommend_add": "",  # 👍
                "recommend_subtract": "",  # 👎
            }
            item = {
                "from_url": url,
                "sku": "",
                "grap_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "version": "1",
                "user": user_info,
                "unique": "",  # TODO
                "element": "",
                "comment": "",
                "reply": reply,
                "pid": pid,
            }
            self.save(item)

    def parse_element(self, selector, item_before, url):
        """
        解析正文内容
        :return:
        """
        global element_unique

        last_modify_time = selector.xpath('.//*[@class="authi"]/em[2]/span/@title')
        if not last_modify_time:
            last_modify_time = selector.xpath('.//*[@class="authi"]/em[2]/span/text()')
        if last_modify_time:
            str_posting_time = str(last_modify_time[0])
            tmp_time = datetime.datetime.strptime(str_posting_time, '%Y-%m-%d %H:%M:%S')
            last_modify_time = int(tmp_time.timestamp()) * 1000
            last_modify_time_fmt = str_posting_time
        else:
            last_modify_time = ""
            last_modify_time_fmt = ""

        user_logo = selector.xpath('.//*[@class="authi"]/a[@rel="nofollow"]/img/@src')
        if user_logo:
            user_logo = user_logo[0]
        else:
            user_logo = ""

        come_from = selector.xpath('.//*[@class="fmty"]/text()')
        if come_from:
            come_from = re.sub(r"\s|\n|\t", "", come_from[0])
        else:
            come_from = ""

        content = selector.xpath(".//*[@class='t_fsz']//td[@class='t_f']")
        if content:
            content = content[0].xpath('string(.)')
        else:
            content = ""

        page_source = selector.xpath(".//*[@class='t_fsz']//td[@class='t_f']")
        page_source = self.deal_page_source(page_source)

        favorite_number = selector.xpath('.//*[@id="favoritenumber"]/text()')
        if favorite_number:
            favorite_number = favorite_number[0]
        else:
            favorite_number = ""

        recommend_add = selector.xpath('.//*[@id="recommendv_add"]/text()')
        if recommend_add:
            recommend_add = recommend_add[0]
        else:
            recommend_add = ""

        recommend_subtract = selector.xpath('.//*[@id="recommendv_subtract"]/text()')
        if recommend_subtract:
            recommend_subtract = recommend_subtract[0]
        else:
            recommend_subtract = ""

        uid_url = selector.xpath('.//*[@class="authi"]/a/@href')
        if uid_url:
            uid_url = uid_url[0]

            user_final_url = urljoin(url, uid_url)
            params = {
                "ajaxmenu": "1",
                "inajax": "1",
                "ajaxtarget": "ajaxid_{}_menu_content".format(random.random()),
            }
            user_info = self.get_user_info(user_final_url, params)
        else:
            user_info = {}

        s = sha1()
        posting_title = item_before.get('posting_title')
        u_name = item_before.get('user_info').get('u_name')
        s.update((posting_title + u_name + content).encode())
        unique = s.hexdigest()

        # 回复相关信息  start
        comment_list = selector.xpath('.//*[@class="cm commentlist"]/div')
        for comment_info in comment_list:
            self.parse_reply(comment_info, url, unique, item_before)

        collection_number = selector.xpath('.//*[@id="collectionnumber"]/text()')
        if collection_number:
            collection_number = collection_number[0]
            pid = "0"
            element_unique = unique
            element = {
                "user_logo": user_logo,
                "come_from": come_from,
                "last_modify_time": last_modify_time,
                "last_modify_time_fmt": last_modify_time_fmt,
                "content": content,
                "page_source": page_source,
                "favorite_number": favorite_number,
                "collection_number": collection_number,
                "recommend_add": recommend_add,  # 👍
                "recommend_subtract": recommend_subtract,  # 👎
            }
            comment = ""
        else:
            pid = element_unique
            element = ""
            comment = {
                "user_logo": user_logo,
                "come_from": come_from,
                "last_modify_time": last_modify_time,
                "last_modify_time_fmt": last_modify_time_fmt,
                "content": content,
                "page_source": page_source,
                "favorite_number": favorite_number,
                "collection_number": collection_number,
                "recommend_add": recommend_add,
                "recommend_subtract": recommend_subtract,
            }

        item = {
            "from_url": url,
            "sku": "",
            "grap_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "version": "1",
            "user": user_info,
            "unique": unique,
            "element": element,
            "comment": comment,
            "reply": "",
            "pid": pid,
        }
        self.save(item)

    def run(self):
        while True:
            # get_reply_ajax 获取多页回复内容
            # get_user_info 获取用户详情信息

            # sum_page = ""                        # 1 获取待爬取帖子信息
            # for page in range(1, sum_page + 1):  # 2 获取帖子页数信息
            #     self.get_replies_full()          # 3 获取帖子
            #         self.parse_element()         # 4 获取内容信息 评论信息
            #           self.parse_reply()         # 5 获取回复信息
            pass


if __name__ == '__main__':
    gzh = HUAWEI('full')
    gzh.run()
