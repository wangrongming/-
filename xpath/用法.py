# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/11/19 11:23
 @Auth : 明明
 @IDE  : PyCharm
 """
# starts-with 顾名思义，匹配一个属性开始位置的关键字
#
# contains 匹配一个属性值中包含的字符串
#
# text（） 匹配的是显示文本信息，此处也可以用来做定位用
#
# eg
#
# //input[starts-with(@name,'name1')]     查找name属性中开始位置包含'name1'关键字的页面元素
#
# //input[contains(@name,'na')]         查找name属性中包含na关键字的页面元素
#
# <a href="http://www.baidu.com">百度搜索</a>
#
# xpath写法为 //a[text()='百度搜索']
#
# 或者 //a[contains(text(),"百度搜索")]

# 兄弟节点 following-sibling::div[1]

# xpath =》html
# base_guarantee = tostring(base_guarantee[0], pretty_print=True, method='html').decode("utf-8")
# base_guarantee = html.unescape(base_guarantee)

# xpath =》删除子标签
# info.getparent().remove(info)
