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

# iqoo店铺
url1 = r"""https://talk8admin.suning.com/yunxin-admin-web/chat/keyWordShopChat.htm?pageFlag=ziying&memberId=&memberName=&memberNick=&memberContact=&custSrvId=&custSrvNick=&reviewRank=&evalTheme=&businessId=&userType=&chatFlags=&chatKeyword=&chatStartTime=2020-06-15+00%3A00%3A00&chatEndTime=2020-06-15+16%3A26%3A50&pageNumberZY=1"""
url_encode = r"""iQOO%E5%AE%A2%E6%9C%8D"""
# print(info)
# info = parse.quote(url1)
# print(info)

info = parse.unquote(url1)
# info = info.encode("utf-8").decode("unicode_escape")
print(info)
