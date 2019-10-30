# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/10/28 10:13
 @Auth : 明明
 @IDE  : PyCharm
 """
import requests

url = "http://www.jiuxian.com/goods-54855.html"

querystring = {"src":"4766","source": "51"}

headers = {
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Host': "www.jiuxian.com",
    # 'Cookie': "__jsluid_h=5405b9a7476862810c3d407b3e2a1408",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)