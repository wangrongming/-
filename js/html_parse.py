# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2020/7/27 14:21
 @IDE  : PyCharm
 """

info = """
var x = document.querySelectorAll('div > div > div > div > div.jSearchList > div.j-module > div.jSearchListArea > div.j-module > ul > li ');
var i;
var info = {};
for (i = 0; i < x.length; i++) {
    var y = x[i].querySelector('div > div.jPic > span');
    var title = x[i].querySelector('div > div.jGoodsInfo > div.jDesc > a');
	
}
console.log(info);
"""
