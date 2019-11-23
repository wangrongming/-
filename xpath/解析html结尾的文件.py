# coding:utf-8
import re
from urllib.parse import urljoin

from lxml import etree

base_url = "https://club.huawei.com/forum.html"

selector = etree.parse(r'D:\code\block\xpath\html\html.html', etree.HTMLParser(encoding='utf-8'))
li_info = selector.xpath('//*[@id="ct"]/div[@class="mn"]/div[@class="fl bm ebbs"]/div')
for model_info in li_info:
    model_li = model_info.xpath(".//td")
    for model in model_li:
        block_url = model.xpath("./dl/dt/a/@href")
        if block_url:
            block_url = urljoin(base_url, block_url[0])
        else:
            continue

        block_name = model.xpath("./dl/dt/a/text()")
        if block_name:
            block_name = block_name[0]
        else:
            block_name = ""

        anti_count_day = model.xpath("./dl/dt/em/text()")
        if anti_count_day:
            anti_count_day = re.sub(r"\s|\n|\t|\(|\)", "", anti_count_day[0])
        else:
            anti_count_day = ""

        print(block_name, block_url, anti_count_day)
        # print(anti_count_day)
