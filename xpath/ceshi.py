# coding:utf-8
from lxml import etree

info = etree.parse(r'D:\code\block\xpath\html\one.html', etree.HTMLParser(encoding='utf-8'))
li_info = etree.HTML('//ul/li')
li_info = etree.HTML("//li")
print(len(li_info))
for info in li_info:
    publish_logo = info.xpath('./div/div[@class="img-box"]/a/img/@src')
    publish_logo = info.xpath('./div/@class')
    # if publish_logo:
    #     publish_logo = publish_logo[0]
    # else:
    #     publish_logo = ""

    gzh_nick_name = ""
    gzh_desc = ""
    gzh_code = ""
    gzh_authentication = ""
    recent_article = ""
    recent_article_url = ""
    publish_time = ""
    publish_month_count = ""
    item = {
        "publish_logo": publish_logo,
    }
    print(item)
