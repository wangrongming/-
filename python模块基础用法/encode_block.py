# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/10/25 18:36
 @Auth : 明明
 @IDE  : PyCharm
 """
from urllib import parse

# 转码
import requests

# print(ord("底"))
# 解码
# print(chr(24213))
# chr(int(k.replace('uni', '0x'), 16))

url = r"https://list.jd.com/list.html?cat=9987,653,655&ev=244%5F124085%4013519%5F73965%40559%5F122032&sort=sort_rank_asc&trans=1&JL=3_%E7%83%AD%E7%82%B9_%E8%B6%85%E9%AB%98%E5%B1%8F%E5%8D%A0%E6%AF%94#J_crumbsBar"
url = r"/list.html?cat=9987,653,655&ev=exbrand%5F8557%403753%5F1097&sort=sort_rank_asc&trans=1&JL=3_运行内存_3GB"
info = parse.unquote(url)


# print(info)


def one_test():
    for i in range(5):
        yield str(i) + "i"

    for j in range(5):
        yield str(j) + "j"


def two_test():
    for i in one_test():
        print(i)


import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def test_three():
    url = "https://list.tmall.com/spu_detail.htm?spuid=1398186641"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
                  'webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': "cna=YOIqFqvLJS0CARsmIBhFiPPu;t=4ee282f04687c3faf20b35b17f8b4b8c;_tb_token_=f37e337e85651;cookie2=12f7a4addb46c85b5f71d6eff1fbeb0d;pnm_cku822=;cq=ccp%3D1;uc1=cookie14=UoTbmhTwOJfyXg%3D%3D&lng=zh_CN;csg=1ed060eb;unb=2200784750096;sn=oppo%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E7%BE%8A%E7%BE%8A;x5sec=7b2273686f7073797374656d3b32223a223534653732346639383635336232623934633839613966326662633239616561434d4c566c764146454d6e47734e72456871447272674561447a49794d4441334f4451334e5441774f5459374d513d3d227d;enc=Q09EpQlwxzHjgzavC%2BDWVuGuPY3mtSzIpnVDi8eiXMnnC59c%2FOFHX93%2FWc5s6yUROoyoVACXZNhrnSPD%2FtiJ6Q%3D%3D;isg=BMPDNXTgmS8q81VcB6PzJuEWUoetkDlPxJjbOvWgHyKZtOPWfQjnyqEiLgRfFK9y;l=cB_gd6zlQOAeiGNMKOCwourza77OSIRAguPzaNbMi_5aL6L6NDQOobsFgFp6VjWdtbYB4cULng29-etkiUa1CLMUd9hG.",
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }
    res = requests.get(url=url, headers=headers, verify=False)
    print(res.text)


from fake_useragent import UserAgent

ua = UserAgent()

if __name__ == '__main__':
    print(ua.random)
