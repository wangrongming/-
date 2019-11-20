# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/10/25 18:36
 @Auth : 明明
 @IDE  : PyCharm
 """
# 转码
print(ord("底"))
# 解码
# print(chr(24213))
# chr(int(k.replace('uni', '0x'), 16))

from urllib import parse

url = r"https://mp.weixin.qq.com/rr?timestamp=1574234110\\x26src=11\\x26ver=1\\x26signature=RlBgYBPxHBk6U*7fz-0FO8YZgGQVtu67IovaDNhjxrSKWdGngNH7Wye*Fb6h-nAd6aTD*fjwfc9S7Esa*DqhTlvfq6x6sT*yeXjI1HDGfsQ="
info = parse.unquote(url)
print(info)
