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

url = r"https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=&t=&sign=&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=&data=%7B\"itemNumId\"%3A\"606336930383\"%7D "
url1 = r"""
%5Cu5C0F%5Cu5361_tb
"""

# print(info)
# info = parse.quote(url1)
info = parse.unquote(url1)
info = info.encode("utf-8").decode("unicode_escape")
print(info)
