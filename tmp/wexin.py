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
    import requests

    url = "https://mp.weixin.qq.com/s"
    url = "http://mp.weixin.qq.com/s?src=11&timestamp=1575546541&ver=2016&signature=a2tDfrdS0pgZXYuUoM*SpnRgWZst0VvixxExLUQ3FV0nexOwPoGIeRbk*VyB6oI*Oo8*0MznRLYGGxjRNct-Mj8Z5fkIySSCboFOyygfHQ*cbgNnYMIjT0w4B3RUFVC-&new=1"

    # querystring = {"src": "11", "timestamp": "1575451801", "ver": "2014",
    #                "signature": "8SIqn7UXCr9XBQGhGbqItrqaICTpCIBAERjCP-U%2AeDUna7v9%2Ae9YcjbPCBPxP1%2A6cSA%2ASudeIIoi2AkbpbzIBD6nPeReNgF5AXqWTOhgO7Y=",
    #                "new": "1"}

    headers = {
        'authority': "mp.weixin.qq.com",
        'cache-control': "max-age=0,no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'sec-fetch-site': "cross-site",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        # 'cookie': "pgv_pvi=1434090496; pgv_pvid=3882778600; rewardsn=; wxtokenkey=777,pgv_pvi=1434090496; pgv_pvid=3882778600; rewardsn=; wxtokenkey=777; rewardsn=; wxtokenkey=777",
        'Postman-Token': "79aae921-da34-4ecc-a600-a76d35144051,9029184d-aefc-47b2-939b-653105ee5f06",
        'Host': "mp.weixin.qq.com",
        'Connection': "keep-alive"
    }
    response_time = CodeTimer()
    with response_time:
        response = requests.request("GET", url, headers=headers, proxies=proxies)
        # response = requests.request("GET", "https://www.baidu.com", proxies=proxies)
    print("response_time.get_cookie.usetime", response_time.usetime)

    print(response.status_code)


if __name__ == '__main__':
    get_proxy("1")
    # get_detail()
    get_index()
