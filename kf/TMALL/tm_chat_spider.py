# encoding: utf-8
"""
@author: Liu
@file: chat_spider.py
@time: 2019/9/18 10:44 AM
"""
import hashlib
import json
import os
import random
import sys
import traceback

import tenacity
from tenacity import stop_after_attempt, wait_fixed

sys.path.append(os.path.abspath("../.."))
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("."))
import requests
import re
import time
import datetime
import click
from data_tool.setting import txt_path
# from ..settings import cellphone_regex
from TMALL.login import run as tmall_login
from data_tool.kafka_template import KafkaTemplate
from lxml import etree

cellphone_regex = r'([1][3-9][0-9]{9})'


# COOKIE = cookie


class TMALLKFSPIDER:

    def __init__(self, shop_name, username, start_time, end_time, kafka, topic):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }
        self.waiter_url = 'https://zizhanghao.taobao.com/subaccount/monitor/chat_record_query.htm?'
        self.customer_url = 'https://zizhanghao.taobao.com/subaccount/monitor/chatRecordJson.htm?'
        self.chat_url = 'https://zizhanghao.taobao.com/subaccount/monitor/chatRecordHtml.htm?'
        self.start_time = start_time
        self.end_time = end_time
        self.shop_name = shop_name
        self.username = username

        self.cache = set()
        self.kafka_template = KafkaTemplate(kafka)
        self.topic = topic
        self.login_cookie = None

    def login(self):
        username = USERNAME
        password = PASSWORD
        url = 'https://zizhanghao.taobao.com/subaccount/monitor/chat_record_query.htm?spm=a211ki.11005426.a311j.2.5d0961c41j5NBK'
        old_cookie = tmall_login(username, password, url)[1]

        COOKIE = ''
        for i in old_cookie:
            COOKIE += i + '=' + old_cookie[i] + ';'
        return COOKIE

    def getBetweenDay(self):
        date_list = []
        begin_date = datetime.datetime.strptime(self.start_time, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(self.end_time, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    def get_waiter(self, timeinfo):
        time.sleep(10)
        start_time = timeinfo
        end_time = timeinfo
        """
        获取客服列表
        :return:
        """
        waiter_res = self.req(self.waiter_url, req_type='get').text
        waiter_list = re.findall(r'option value="(.*?)"', waiter_res)
        print("查看客服列表： {}".format(waiter_list))
        main_customer = waiter_list[0]
        for chat_arg in [(waiter, start_time, end_time, 'null', main_customer) for waiter in waiter_list
                         if
                         waiter != main_customer]:
            self.get_customer(chat_arg)

    def get_customer(self, args):
        """
        获取当前客服对应的客户列表
        :return:
        """
        waiter = args[0]
        start_time = args[1]
        end_time = args[2]
        beginkey = args[3]
        main_customer = args[4]
        data = {
            'action': '/subaccount/monitor/ChatRecordQueryAction',
            'eventSubmitDoQueryChatRealtion': 'anything',
            '_tb_token_': re.search(r'_tb_token_=(.*?);', self.headers['cookie']).groups()[0],
            '_input_charset': 'utf-8',
            'chatRelationQuery': f'{{"employeeNick":"{waiter}","customerNick":"","start":"{start_time}","end":"{end_time}","beginKey":{beginkey},"endKey":null,"employeeAll":false,"customerAll":true}}',
            'site': 0,
            '_': int(time.time() * 1e3)
        }
        time.sleep(random.randint(5000, 9000) / 1000)
        res = self.req(self.customer_url, req_type='get', data=data)
        if "employeeUserNicks" not in res.text:
            print("employeeUserNicks is None:", res.text)
            return
        new_waiter_name = res.json()['employeeUserNicks'][0]
        customerusernicks_list = res.json()['customerUserNicks']
        chat_arg_list = [(new_waiter_name, customer, start_time, end_time, main_customer) for customer in
                         customerusernicks_list if customer not in self.cache]

        # 数据存储
        for chat_arg in chat_arg_list:
            self.get_chat(chat_arg)

        hasnextpage = res.json()['hasNextPage']
        if hasnextpage:
            endKey = res.json()['endKey']
            self.get_customer((waiter, start_time, end_time, f'"{endKey}"', main_customer))

    def get_chat(self, arg):
        """
        获取聊天记录
        :return:
        """
        waiter = arg[0]
        customer = arg[1]
        start_time = arg[2]
        end_time = arg[3]
        main_customer = "cntaobao" + arg[4]
        self.cache.add(customer)
        print(waiter, customer, start_time)
        data = {
            'action': '/subaccount/monitor/ChatRecordQueryAction',
            'eventSubmitDoQueryChatContent': 'anything',
            '_tb_token_': re.search(r'_tb_token_=(.*?);', self.headers['cookie']).groups()[0],
            '_input_charset': 'utf-8',
            'chatContentQuery': f'{{"employeeUserNick":["{main_customer}"],"customerUserNick":["{customer}"],"employeeAll":false,"customerAll":false,"start":"{start_time}","end":"{end_time}","beginKey":null,"endKey":null}}',
            'site': 0,
            '_': int(time.time() * 1e3)
        }
        time.sleep(random.randint(10, 20) / 1000)
        res = self.req(self.chat_url, 'get', data)
        chat_time = self.deal_start_time(res.text)
        if "暂无聊天记录" in res.text or not chat_time:
            return None
        item = {}
        item['insert_timestamp'] = int(time.time() * 1e3)
        item['grap_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        item['from_url'] = str(res.url)
        item['shop_name'] = self.shop_name
        item['source_id'] = 3
        item['username'] = self.username
        item['waiter'] = main_customer
        item['customer'] = customer
        item['chat_time'] = chat_time
        item['chat_info'] = res.text

        phone_num_list = re.findall(cellphone_regex, res.text)
        for phone_num_str in phone_num_list:
            item['chat_info'] = item['chat_info'].replace(phone_num_str,
                                                          phone_num_str[:3] + '******' + phone_num_str[-2:])

        customer = re.sub("cntaobao", "", customer)
        chat_info = res.text
        if customer not in chat_info:
            return

        item['sid'] = self.md5_gen(item['chat_info'])
        try:
            self.send_data(item)
            # print(item)
            pass
        except Exception:
            print("repr(item)", repr(item))
            print(traceback.format_exc())
            raise Exception

    def send_data(self, item):
        url = "http://127.0.0.1:30006/save/service"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }
        res = requests.post(url=url, headers=headers, data=json.dumps(item, ensure_ascii=False).encode("utf-8"))
        if str(res.text) != "1":
            print("调用数据存储接口错误")

    def is_need_login(self, res):
        if not res.text:
            return
        if "手机扫码，安全登录" in res.text:
            print("cookie过期需要重新登录")
            self.login_cookie = self.login()
            raise Exception

    @staticmethod
    def deal_start_time(info):
        """
        解析文本 获取回话开始时间
        :param info:
        :return:
        """
        sel = ""
        try:
            if "暂无聊天记录" in info:
                return ""
            sel = etree.HTML(info)
            sel = sel.xpath("//div[@class='chatlog-list']/p")
            chat_date = sel[0].xpath("./text()")
            chat_hour = sel[1].xpath("./text()")
            chat_date = re.sub(r"\s|\n", "", chat_date[0])
            chat_hour = re.sub(r"\s|\n|(.*?\()|\)", "", chat_hour[0])
            start_time = chat_date + " " + chat_hour
            return start_time
        except IndexError:
            print(info, sel)
            return ""

    @tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1))
    def req(self, url, req_type, data=None):
        if req_type == 'get':
            while True:
                self.headers['cookie'] = self.login_cookie
                try:
                    res = requests.get(url, params=data, headers=self.headers, timeout=3)
                    self.is_need_login(res)
                    return res
                except requests.exceptions.RequestException:
                    time.sleep(0.01)
        else:
            while True:
                self.headers['cookie'] = self.login_cookie
                try:
                    res = requests.post(url, data=data, headers=self.headers, timeout=3)
                    self.is_need_login(res)
                    return res
                except requests.exceptions.RequestException:
                    time.sleep(0.01)

    @staticmethod
    def md5_gen(info):
        m = hashlib.md5()
        m.update(repr(info).encode(encoding='utf-8'))
        hex_info = m.hexdigest()
        return hex_info

    def run(self):

        date_list = reversed(self.getBetweenDay())
        for date in date_list:
            try:
                self.login_cookie = self.login()
                self.cache.clear()
                self.get_waiter(date)
            except:
                print(traceback.format_exc())


def parse_members():
    with open("{}/tm_member.txt".format(txt_path), "r", encoding='utf-8') as f:
        member_li = []
        for line in f:
            line = re.sub(r"\n|\t|\s", "", line)
            if not line:
                continue
            info = line.split("----")
            member_li.append(info)
        return member_li


@click.command()
@click.option('--start_time', default='2019-11-01', type=str, help='起始时间')
@click.option('--end_time', default='2019-11-10', type=str, help='结束时间')
@click.option('--username', default='', type=str, help='要登陆的账户名')
@click.option('--password', default='', type=str, help='要登陆的密码')
@click.option('--shop_name', default='', type=str, help='要爬取店铺名称')
@click.option('--kafka', default='192.168.0.158:9092', type=str, help='kafka地址:port')
@click.option('--topic', default='DATA_SECURITY_FILTER', type=str, help='kafka队列名称')
def main(shop_name, start_time, end_time, username, password, kafka, topic):
    for i in range(2):
        global USERNAME, PASSWORD
        if username and password:
            USERNAME = username
            PASSWORD = password
            tmall = TMALLKFSPIDER(shop_name, username, start_time, end_time, kafka, topic)
            tmall.run()
        else:
            for members in parse_members():
                print("|{}|".format(members[0]), "|{}|".format(members[1]), "|{}|".format(members[2]))
                USERNAME = re.sub(r"\s|\n|\t", "", members[1])
                PASSWORD = re.sub(r"\s|\n|\t", "", members[2])
                tmall = TMALLKFSPIDER(members[0], members[1], start_time, end_time, kafka, topic)
                tmall.run()


if __name__ == '__main__':
    main()
