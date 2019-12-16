import json
import logging
import platform
import time
import traceback

import requests

logger = logging

if 'Win' in platform.system():
    proxy_url = 'http://proxy.yuntingai.com/proxy/getProxy/26'
else:
    proxy_url = 'http://10.1.6.218/proxy/getProxy/26'

cookies_login = {}
proxies = {}


def get_proxy(retry_state):
    global proxies
    while True:
        try:
            res = requests.get(proxy_url, timeout=3)
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
                print(proxies)
                break
            else:
                logger.info("当前获取ip代理 没有真实ip")
                time.sleep(2)
                continue
        except Exception:
            logger.error(traceback.format_exc())
            time.sleep(3)


class CodeTimer(object):
    """
    用上下文管理器计时
    """

    def __enter__(self):
        self.t0 = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.usetime = time.time() - self.t0


def get_index():
    url = "https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E9%AD%85%E6%97%8F&ie=utf8&_sug_=n&_sug_type_="

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'weixin.sogou.com',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }

    response = requests.request("GET", url, headers=headers, proxies=proxies, timeout=10)
    # response = requests.request("GET", url, headers=headers, proxies=None)

    text = response.content.decode("utf-8")
    if "我们的系统检测到您网络中存在异常访问请求" in text:
        print("弹出验证码")
    else:
        print("请求成功")


def get_detail():
    url = "https://list.tmall.com/search_product.htm?spm=875.7931836/B.subpannel2016052.1.51104265S8hyMZ&pos=1&cat=50928001&vmarket=97602&theme=699&acm=2016030725.1003.2.709584&scm=1003.2.2016030725.OTHER_1551655766374_709584"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'cna=YOIqFqvLJS0CARsmIBhFiPPu; _med=dw:1920&dh:1080&pw:1920&ph:1080&ist:0; cq=ccp%3D1; t=24a7aa03e525d84915143074b5bdbec7; enc=zASu8fjs%2B%2BH5sTxq6BE98Xe8TbAQQ1QQ8c9NdXQiulT7kRkUr6%2F9BNMokLyezPC%2BhMwZlS71yh30JEz3q7jyog%3D%3D; _tb_token_=361590e05316; cookie2=139e3c8bf7051a991962c80399ff6539; _m_h5_tk=9e9bce723d955007a943b6df9d55dd6d_1576048332169; _m_h5_tk_enc=b5a5553f85b64bd032ec5aeacf1b9a5a; _uab_collina=157604556981314367496318; res=scroll%3A1903*5958-client%3A1903*937-offset%3A1903*5958-screen%3A1920*1080; pnm_cku822=098%23E1hvg9vUvbpvUvCkvvvvvjiPRsdv6jlnRsqhgjthPmPZ1jYjPFMvzjtnR2SW1jYn2QhvCvvvMMGCvpvVvUCvpvvvmphvLvj2I8vag8g7%2BulgENoxdBeKHkx%2F1j7J%2Bu6wjLVxfBAK5u6aWXxrV4TJRAYVyOvOHd8rwAq61C4AdB9aUWLUjC4AdcwuYU9BHd8raoktvpvIvvCvpvvv96vvvhNjvvmClvvvBGwvvvUwvvCj1Qvvv99vvhNjvvvmmUyCvvOCvhE2znAivpvUvvCCbG%2FuA26tvpvhvvCvp8wCvvpvvhHh; l=dBN8xeNRqtdrOzQBBOCgiuIRuFQ9OIRAguPRwtGpi_5CV1T6KnbOkEUhte96cjWfG08B4cULng29-etkiE9UIe60ll2zUxDc.; isg=BI6OUaSiXwkbQesysBgzbQfq32SQpzw8MYdGebjX2xFMGy51IJ-FGY7ZUwfSA0oh',
        'referer': 'https://www.tmall.com/?spm=a220m.1000858.a2226n0.1.194476d54GOUWJ',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }
    res = requests.get(url=url, headers=headers, proxies=proxies, timeout=5)
    text = res.text
    if "亲，小二正忙" in text:
        print("亲，小二正忙")
        raise Exception

    if "请输入密码" in text:
        print("输入密码提示")
        raise Exception

    if res.status_code != 200:
        print("返回404")
        raise Exception

    print(res.text)
    print("访问成功")


def send_data(item):
    url = "http://192.168.110.80:30006/save/service"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
    }
    data = item
    res = requests.post(url=url, headers=headers, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    print(res.text)


if __name__ == '__main__':
    get_proxy("1")
    # for i in range(1):
    #     get_detail()
    # get_index()
    # for i in range(10):
    #     item = {
    #         "insert_timestamp": 1576303699108,
    #         "grap_time": "2019-12-14 14:08:19",
    #         "from_url": "https://zizhanghao.taobao.com/subaccount/monitor/chatRecordHtml.htm?action=%2Fsubaccount%2Fmonitor%2FChatRecordQueryAction&eventSubmitDoQueryChatContent=anything&_tb_token_=e8e303ebee4ee&_input_charset=utf-8&chatContentQuery=%7B%22employeeUserNick%22%3A%5B%22cntaobaooppo%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%22%5D%2C%22customerUserNick%22%3A%5B%22cntaobaooppo%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E5%87%8C%E5%87%8C%22%5D%2C%22employeeAll%22%3Afalse%2C%22customerAll%22%3Afalse%2C%22start%22%3A%222019-11-30%22%2C%22end%22%3A%222019-11-30%22%2C%22beginKey%22%3Anull%2C%22endKey%22%3Anull%7D&site=0&_=1576303698197",
    #         "shop_name": "oppo官方旗舰店",
    #         "source_id": 3,
    #         "username": "oppo官方旗舰店:羊羊",
    #         "waiter": "cntaobaooppo官方旗舰店",
    #         "customer": "cntaobaooppo官方旗舰店:凌凌",
    #         "chat_time": "2019-11-30 17:04:43",
    #         "chat_info": "div class=",
    #         "sid": "3f16624c357075d8bf59f7461faa6e0a"
    #     }
    #     send_data(item)
