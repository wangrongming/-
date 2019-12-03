# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/10/28 10:13
 @Auth : 明明
 @IDE  : PyCharm
 """
import requests

proxies = {'https': '106.125.238.53:4352', 'http': '106.125.238.53:4352'}
# proxies = {'https': 'https://106.125.238.53:4352', 'http': 'http://106.125.238.53:4352'}
info = requests.get(url='https://www.baidu.com',
                    proxies=proxies,
                    timeout=3).content.decode(
    'utf-8')

print(info)
