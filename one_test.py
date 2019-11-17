import re

import execjs
import requests


def with_params():
    command = """
    function add (x, y){
        return x+y;
    };
    """
    ctx = execjs.compile(command)
    return ctx.call("add", 2, 2)


def get_k_h(url):
    b = 69
    a = url.find("url=")
    url = url + "&k=" + str(b) + "&h=" + url[a + 4 + 21 + b: a + 4 + 21 + b + 1]
    return url


def url_js_index(href):
    command = """
    function gen_url(href) {
    var b = 69,
    a = href.indexOf("url="),
    c = href.indexOf("&k="); 
    - 1 !== a && -1 === c && (a = href.substr(a + 4 + parseInt("21") + b, 1), href += "&k=" + b + "&h=" + a)
    return href
};"""
    ctx = execjs.compile(command)
    return ctx.call("gen_url", href)


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
    import requests

    url = "https://weixin.sogou.com/weixin"

    querystring = {"type": "2", "query": "%E5%B0%8F%E7%B1%B3", "ie": "utf8", "s_from": "input", "_sug_": "n",
                   "_sug_type_": "1", "w": "01015002", "oq": "", "ri": "0", "sourceid": "sugg", "sut": "0",
                   "sst0": "1573658029796", "lkt": "0%2C0%2C0", "p": "40040108"}
    cookie = "ABTEST=0|1573748825|v1; SNUID=9435283A4B49DC1BB8FABDC94C4E845E; IPLOC=CN4403; SUID=D87E63714A42910A000000005DCD8059; SUID=D87E63715118910A000000005DCD8059; JSESSIONID=aaaOJbelYL_GkhOE8ex4w"
    headers = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Referer': "https://weixin.sogou.com/",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cookie': cookie,
        'Host': "weixin.sogou.com",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    li = re.findall(r'<h3>.*?<a.*?href="(.*?)".*?h3>', response.text, re.S)
    for href in li:
        # '/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgSxQRnYriDKi1ktpM-rdX9YjZObk4AYOjx1qXa8Fplpd9SW0vaJ2asCcOs1n6j8_NvyHIvUjdOBoDPp0guli4gGkLTV9_mHCVqTmfrwcytELbf7l8wU6v8XRc-7ChACC9o_ck4Uq9Lym1w3-d_LlS9dqG4F5OF7SWTXwPFr3m7XkcvOpoOut2oMVwqo6om42Y0Nd9L2ITgxfxTLrQeKzuPyctPujwwRB2Pw..&amp;type=2&amp;query=%E5%B0%8F%E7%B1%B3'
        href = "https://weixin.sogou.com" + href
        detail_one(response.url, href, cookie)


def detail_one(refrer, url, cookie):
    if not url:
        url = "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS8HPlqRsn9otcJAb5t4tbPWTNJPXjmQUdVqXa8Fplpd9Z3Dooyeznbhkz_lgSFFvLel0j-ysgjFZPbVk6WxGvRpMxigcZt7F4JOXH1XZgj6ToWnH0q2O0zXui_-cUViHF1JnlapW9UKYwEG2iyvGfh4hUs81ZCzL5EWYq19y75jT0kcUI7b2HUCiIbQD93oyEi7EofnpKeF3TiIlBlz5hvEHpHkoPMgL3A..&type=2&query=%E5%B0%8F%E7%B1%B3&k=59&h=j"
    headers = {
        'Host': 'weixin.sogou.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': refrer,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookie,
        # 'Cookie': "rewardsn=; wxtokenkey=777",
    }
    response = requests.request("GET", url, headers=headers)
    print(response.text[:200])
    print(1)
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
    # print(with_params())
    href = "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS_yOFgPamohIURzt-uiC_7jWUCR_KqtUqVqXa8Fplpd94ucNnOm3i8_HNKZNA2Z3Kl1p2y_k5ar2QBhCj2IqmNzpV7uzAmfOOY17KoiHMXaB57uzUeVDyoQy0bQ6Wu52hEQF0medwUKuyJSiks_DoP6eWBQz-wM3wGL2hPPk3h41QqAWQYUJnM3rOfHHyBpLfpfXSGeZfw4Q6b5lbYXlo_15LU3lqtPw9g..&type=2&query=%E6%9F%AC%E5%9F%94%E5%AF%A8"
    print(url_js_index(href))
    print(get_k_h(href))
# index_one()
# detail_one_res = detail_one()
# print(detail_one_res)
# detail_two(detail_one_res)
