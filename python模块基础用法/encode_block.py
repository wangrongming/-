# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/10/25 18:36
 @Auth : 明明
 @IDE  : PyCharm
 """
from urllib import parse

# 转码

# print(ord("底"))
# 解码
# print(chr(24213))
# chr(int(k.replace('uni', '0x'), 16))

# 16进制转化未中文
# info.encode("utf-8").decode("unicode_escape")

url1 = r"""%B6%FA%BB%FA"""
url_encode = r"""%B6%FA%BB%FA"""
# print(info)
info = parse.quote(url1)
print(info)

info = parse.unquote(url1)
# info = info.encode("utf-8").decode("unicode_escape")
print(info)
