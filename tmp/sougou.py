# coding=utf-8

import json
import platform
import random
import re
import time
import traceback
from urllib import parse

import requests
from lxml import etree

# ssl._create_default_https_context = ssl._create_unverified_context
proxies = {}

if 'Win' in platform.system():
    proxy_url = 'http://proxy.yuntingai.com/proxy/getProxy/29'
else:
    proxy_url = 'http://10.1.6.218/proxy/getProxy/29'


class CodeTimer(object):
    """
    用上下文管理器计时
    """

    def __enter__(self):
        self.t0 = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.usetime = time.time() - self.t0


def get_proxy(retry_state):
    global proxies
    while True:
        url1 = proxy_url
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
                print("当前重试次数", retry_state, "当前代理", proxies, "trueIp", proxy_info.get('trueIp'))
                break
            else:
                print("当前获取ip代理 没有真实ip")
                time.sleep(2)
                continue
        except Exception:
            print(traceback.format_exc())
            time.sleep(3)


def get_cookie(response1, uigs_para, UserAgent):
    SetCookie = response1.headers['Set-Cookie']
    cookie_params = {
        "ABTEST": re.findall('ABTEST=(.*?);', SetCookie, re.S)[0],
        "SNUID": re.findall('SNUID=(.*?);', SetCookie, re.S)[0],
        "IPLOC": re.findall('IPLOC=(.*?);', SetCookie, re.S)[0],
        "SUID": re.findall('SUID=(.*?);', SetCookie, re.S)[0]
    }

    url = "https://www.sogou.com/sug/css/m3.min.v.7.css"
    headers = {
        "Accept": "text/css,*/*;q=0.1",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}".format(cookie_params['SNUID'], cookie_params['IPLOC']),
        "Host": "www.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": UserAgent
    }
    response2_time = CodeTimer()
    with response2_time:
        response2 = requests.get(url, headers=headers, proxies=proxies)
    print("response2_time.get_cookie.usetime", response2_time.usetime)

    SetCookie = response2.headers['Set-Cookie']
    cookie_params['SUID'] = re.findall('SUID=(.*?);', SetCookie, re.S)[0]

    url = "https://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}".format(cookie_params['ABTEST'], cookie_params['SNUID'],
                                                                  cookie_params['IPLOC'],
                                                                  cookie_params['SUID']),
        "Host": "weixin.sogou.com",
        "Referer": response1.url,
        "User-Agent": UserAgent
    }
    response3_time = CodeTimer()
    with response3_time:
        response3 = requests.get(url, headers=headers, proxies=proxies)
    print("response3_time.get_cookie.usetime", response3_time.usetime)

    SetCookie = response3.headers['Set-Cookie']
    cookie_params['JSESSIONID'] = re.findall('JSESSIONID=(.*?);', SetCookie, re.S)[0]

    url = "https://pb.sogou.com/pv.gif"
    headers = {
        "Accept": "image/webp,*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}; SUID={}".format(cookie_params['SNUID'], cookie_params['IPLOC'],
                                                       cookie_params['SUID']),
        "Host": "pb.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": UserAgent
    }

    response4_time = CodeTimer()
    with response4_time:
        response4 = requests.get(url, headers=headers, params=uigs_para, proxies=proxies)
    print("response4_time.get_cookie.usetime", response4_time.usetime)
    SetCookie = response4.headers['Set-Cookie']
    cookie_params['SUV'] = re.findall('SUV=(.*?);', SetCookie, re.S)[0]

    return cookie_params


def get_k_h(url):
    b = int(random.random() * 100) + 1
    a = url.find("url=")
    url = url + "&k=" + str(b) + "&h=" + url[a + 4 + 21 + b: a + 4 + 21 + b + 1]
    return url


def get_uigs_para(response):
    try:
        uigs_para = re.findall('var uigs_para = (.*?);', response.text, re.S)[0]
        if 'passportUserId ? "1" : "0"' in uigs_para:
            uigs_para = uigs_para.replace('passportUserId ? "1" : "0"', '0')
        uigs_para = json.loads(uigs_para)
        exp_id = re.findall('uigs_para.exp_id = "(.*?)";', response.text, re.S)[0]
        uigs_para['right'] = 'right0_0'
        uigs_para['exp_id'] = exp_id[:-1]
        return uigs_para
    except Exception as e:
        print("get_uigs_para", response.content.decode("utf-8"))
        raise Exception


def main_v4(list_url, UserAgent):
    main_v4_time = CodeTimer()
    with main_v4_time:
        get_proxy(1)
        headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "weixin.sogou.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": UserAgent,
        }
        response1_time = CodeTimer()
        with response1_time:
            response1 = requests.get(list_url, headers=headers1, proxies=proxies, timeout=10)
        print("response1_time.usetime", response1_time.usetime)

        html = etree.HTML(response1.text)
        urls = ['https://weixin.sogou.com' + i for i in html.xpath('//div[@class="img-box"]/a/@href')]

        uigs_para = get_uigs_para(response1)

        params_time = CodeTimer()
        with params_time:
            params = get_cookie(response1, uigs_para, UserAgent)
        print("params_time.usetime get_cookie总时间", params_time.usetime)

        for url in urls:
            url = get_k_h(url)
            headers3 = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Connection": "keep-alive",
                "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}; JSESSIONID={}; SUV={}".format(params['ABTEST'],
                                                                                                 params['SNUID'],
                                                                                                 params['IPLOC'],
                                                                                                 params['SUID'],
                                                                                                 params['JSESSIONID'],
                                                                                                 params['SUV']),
                "Host": "weixin.sogou.com",
                "Referer": list_url,
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": UserAgent
            }
            response3_time = CodeTimer()
            with response3_time:
                response3 = requests.get(url, headers=headers3, proxies=proxies)
            print("response3_time.usetime", response3_time.usetime)

            fragments = re.findall("url \+= '(.*?)'", response3.text, re.S)
            itemurl = ''
            for i in fragments:
                itemurl += i

            # 文章url拿正文
            headers4 = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "user-agent": UserAgent
            }
            time.sleep(1)
            response4_time = CodeTimer()
            with response4_time:
                response4 = requests.get(itemurl, headers=headers4, proxies=proxies)
            print("response4_time.usetime", response4_time.usetime)
            html = etree.HTML(response4.text)
            # print(response4.text)
            print(response4.status_code)
            print(html.xpath('//meta[@property="og:title"]/@content')[0])
    print("main_v4_time.usetime", main_v4_time.usetime)


if __name__ == "__main__":
    key = "魅族"
    url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=5470&sst0=1575510684847&lkt=4%2C1575510680866%2C1575510681219'.format(
        parse.quote(key))
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    main_v4(url, UserAgent)
