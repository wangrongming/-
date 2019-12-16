import hashlib
import os
import sys
import traceback

sys.path.append(os.path.abspath("../.."))
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("."))

import click
import requests
import time
import datetime
import re
from jsonpath import jsonpath
from multiprocessing import dummy
from JD.login import main as get_cookie
from data_tool.kafka_template import KafkaTemplate
# from settings import cellphone_regex
import json
from data_tool.setting import txt_path

cellphone_regex = r'([1][3-9][0-9]{9})'


def set_proxy():
    while True:
        url1 = 'http://proxy.dataduoduo.com/proxy/getProxy?tid=999'
        try:
            res = requests.get(url1, timeout=3)
        except Exception:
            continue
        if res.status_code != 200:
            continue
        proxy_info = res.json()
        try:
            if proxy_info['isAlive']:
                if proxy_info['type'] == 'http':
                    proxy_info['type'] = 'http'
                else:
                    proxy_info['type'] = 'socks5'
                return {
                    'https': "{}://{}:{}@{}:{}".format(proxy_info['type'], proxy_info['userName'],
                                                       proxy_info['passWord'],
                                                       proxy_info['host'], proxy_info['port']),
                    'http': "{}://{}:{}@{}:{}".format(proxy_info['type'], proxy_info['userName'],
                                                      proxy_info['passWord'],
                                                      proxy_info['host'], proxy_info['port']),
                }
        except TypeError:
            pass


class JDKF:
    def __init__(self, start_time, end_time, username, password, shop_name, worker, mongo, collection, kafka, topic):
        self.start_time = start_time
        self.end_time = end_time
        self.worker = worker
        # self.client = MongoClient("mongodb://{}:{}/KF".format(MONGO_HOST, MONGO_PORT))
        # self.db = self.client.get_database()
        # self.collection = self.db.get_collection(collection)
        self.username = username
        self.shop_name = shop_name
        cookie = get_cookie(username, password)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'cookie': cookie,
            'referer': 'http://xi.jd.com/customerassistant/filterCustomer.html?menu=ddQuery&content=chatLog'
        }
        self.kafka_template = KafkaTemplate(kafka)
        self.topic = topic

    def get_totalpage(self, col_time):
        """
        获取评论总页数
        :return: 总页数
        """
        url = f'http://kf.jd.com/chatLog/queryList.action?page=1&pageSize=5&startTime={col_time}&endTime={col_time}'
        first_page = self.req(url)
        total_page = first_page['totalPage']
        self.save(first_page, url, col_time)
        return total_page

    def get_ltjl(self, arg):
        """
        获取每一页的评论
        :param num: 页码
        :return: 每一页信息
        """
        col_time = arg[0]
        num = arg[1]
        url = f'http://kf.jd.com/chatLog/queryList.action?page={num}&pageSize=5&startTime={col_time}&endTime={col_time}'
        page_info = self.req(url)
        self.save(page_info, url, col_time)

    def getBetweenDay(self):
        date_list = []
        begin_date = datetime.datetime.strptime(self.start_time, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(self.end_time, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    def save(self, page_info, url, col_time):
        print(url)
        chatloglist = jsonpath(page_info, '$..chatLogList')[0]
        for chatlog in chatloglist:
            try:
                item = {}
                chat_list = chatlog['chatLogMessageList']
                if len(chat_list):
                    sid = None
                    for chat in chat_list:
                        if chat.get('sid'):
                            sid = chat['sid']
                        phone_num_str = re.findall(cellphone_regex, chat['content'])[0] if re.findall(cellphone_regex,
                                                                                                      chat[
                                                                                                          'content']) else ''
                        if phone_num_str:
                            chat['content'] = chat['content'].replace(phone_num_str,
                                                                      phone_num_str[:3] + '******' + phone_num_str[-2:])
                    if not sid:
                        continue
                    item['from_url'] = url
                    item['insert_timestamp'] = int(round(time.time() * 1000))
                    item['grap_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    item['version'] = 1
                    item['source_id'] = 1
                    item['sid'] = sid
                    item['chat_time'] = col_time
                    item["_id"] = self.md5_gen(chatlog)
                    item["username"] = self.username
                    item["shop_name"] = self.shop_name
                    item['element'] = chatlog
                    # print(item)
                    # if not self.collection.find_one({"_id": item["_id"]}):
                    #     self.collection.insert_one(item)  # TODO
                    # self.kafka_template.produce(self.topic, json.dumps(item, ensure_ascii=False))
                    self.send_data(item)
            except Exception as e:
                print(traceback.format_exc())
                print(chatlog)
                raise Exception

    def send_data(self, item):
        url = "http://127.0.0.1:30006/save/service"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }
        res = requests.post(url=url, headers=headers, data=json.dumps(item, ensure_ascii=False).encode("utf-8"))
        if str(res.text) != "1":
            print("调用数据存储接口错误")

    @staticmethod
    def md5_gen(info):
        m = hashlib.md5()
        m.update(repr(info).encode(encoding='utf-8'))
        hex_info = m.hexdigest()
        return hex_info

    def req(self, url):
        """
        封装requests模块的使用
        :param url: 请求连接
        :return:.find({end_time:'2019-09-17'})
        """
        while True:
            try:
                res = requests.get(url, headers=self.headers, timeout=3).json()
                return res
            except requests.RequestException:
                time.sleep(1)

    def run(self):
        time_list = self.getBetweenDay()
        for col_time in time_list:
            total_page = self.get_totalpage(col_time)
            print(total_page)
            # for i in range(2, total_page + 1):
            #     self.get_ltjl(i)
            pool = dummy.Pool(self.worker)
            pool.map(self.get_ltjl, [(col_time, i) for i in range(2, total_page + 1)])
            pool.close()
            pool.join()


@click.command()
@click.option('--start_time', default='2019-10-29', type=str, help='起始时间')
@click.option('--end_time', default='2019-10-29', type=str, help='结束时间')
@click.option('--username', default='', type=str, help='要登陆的账户名')
@click.option('--password', default='', type=str, help='要登陆的密码')
@click.option('--shop_name', default='', type=str, help='要爬取店铺名称')
@click.option('--worker', default=1, type=int, help='爬虫节点运行的线程数')
@click.option('--mongo', default='', type=str, help='mongo地址:port')
# @click.option('--mongo', default='mongodb://192.168.0.93:27017/JDKF', type=str, help='mongo地址:port')
# @click.option('--mongo', default='mongodb://10.1.6.173:28018/JDKF', type=str, help='mongo地址:port')
@click.option('--collection', default='jdkf', type=str, help='mongo集合名')
# @click.option('--kafka', default=['10.1.6.25:9092', '10.1.6.24:9092'], type=str, help='kafka地址:port')
@click.option('--kafka', default='192.168.0.158:9092', type=str, help='kafka地址:port')
@click.option('--topic', default='DATA_SECURITY_FILTER', type=str, help='kafka队列名称')
def main(start_time, end_time, username, password, shop_name, worker, mongo, collection, kafka, topic):
    for i in range(2):
        if username and password:
            print(username, password)
            jdkf = JDKF(start_time, end_time, username, password, shop_name, worker, mongo, collection, kafka, topic)
            jdkf.run()
        else:
            for members in parse_members():
                print(members[0], members[1], members[2])
                jdkf = JDKF(start_time, end_time, members[1], members[2], members[0], worker, mongo, collection, kafka,
                            topic)
                jdkf.run()


def parse_members():
    with open("{}/jd_member.txt".format(txt_path), "r", encoding='utf-8') as f:
        member_li = []
        for line in f:
            info = line.split("----")
            member_li.append(info)
        return member_li


if __name__ == '__main__':
    main()
