import re

import execjs
import requests


def url_js(url):
    command = """
    function url (){
        %s
        return url;
    };
    """ % url
    ctx = execjs.compile(command)
    return ctx.call("url")


def url_pattern(text):
    res = re.findall(r"<script>(.*?)url\.replace", text, re.S)
    return res[0]


def index_one():
    pass


def detail_one():
    url = "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS8HPlqRsn9otcJAb5t4tbPWTNJPXjmQUdVqXa8Fplpd9Z3Dooyeznbhkz_lgSFFvLel0j-ysgjFZPbVk6WxGvRpMxigcZt7F4JOXH1XZgj6ToWnH0q2O0zXui_-cUViHF1JnlapW9UKYwEG2iyvGfh4hUs81ZCzL5EWYq19y75jT0kcUI7b2HUCiIbQD93oyEi7EofnpKeF3TiIlBlz5hvEHpHkoPMgL3A..&type=2&query=%E5%B0%8F%E7%B1%B3&k=59&h=j"
    headers = {
        'Host': 'weixin.sogou.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://weixin.sogou.com/weixin?type=2&query=%E5%B0%8F%E7%B1%B3&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&w=01015002&oq=&ri=0&sourceid=sugg&sut=0&sst0=1573658029796&lkt=0%2C0%2C0&p=40040108',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'IPLOC=CN4403; SUID=B72812DA2F20910A000000005DCC0FEB; SUV=1573654502268031; ABTEST=0|1573654510|v1; SNUID=B52A13D80207963BFC1F55A902B1DCED; weixinIndexVisited=1; pgv_pvi=1177630720; sct=2; JSESSIONID=aaaH9-EIE7BZl9SZoex4w',
    }
    response = requests.request("GET", url, headers=headers)
    item = {
        "referer": url,
        "target": url_js(url_pattern(response.text))
    }
    return item


def detail_two(item):
    url = item['target']
    headers = {
        'authority': "mp.weixin.qq.com",
        'cache-control': "max-age=0,no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'referer': item['referer'],
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'cookie': "pgv_pvi=2501053440; pgv_si=s7603036160; pgv_info=ssid=s1978121797; pgv_pvid=437692080; _pcmgr_localtk=FuZ9z!q(Zz; _qpsvr_localtk=)OwsETEZHB; rewardsn=; wxtokenkey=777",
        'if-modified-since': "Wed, 13 Nov 2019 23:13:57 +0800",
        'Host': "mp.weixin.qq.com",
        'Connection': "keep-alive"
    }
    response = requests.request("GET", url, headers=headers)
    print(response.text)


if __name__ == '__main__':
    # index_one()
    detail_one_res = detail_one()
    print(detail_one_res)
    detail_two(detail_one_res)
