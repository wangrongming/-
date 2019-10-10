from lxml import etree

info = etree.parse(r'D:\block\xpath\html.html', etree.HTMLParser(encoding='utf-8'))
sel = info.xpath('//title/text()')
print(sel)