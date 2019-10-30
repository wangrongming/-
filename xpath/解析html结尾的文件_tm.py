from lxml import etree

info = etree.parse(r'D:\code\block\xpath\html\tianmao_oppo.html', etree.HTMLParser(encoding='utf-8'))
sel = info.xpath("//div[@class='J_TItems']/div[@class='item5line1']")
li = []
i = 0
for info_one in sel:
    i += 1
    if i > 12:
        break

    info_one.xpath("./dl[@class='item']")
    for info in info_one:
        href = info.xpath("./dt/a/@href")
        title = info.xpath("./dt/a/img/@alt")
    # href = info.xpath("./div[@class='jItem']/div[@class='jPic']/a/@href")
    # if not href:
    #     href = info.xpath("./div[@class='jItem jCurrent']/div[@class='jPic']/a/@href")
    #
    # title = info.xpath("./div[@class='jItem jCurrent']/div[@class='jGoodsInfo']/div[@class='jDesc']/a/text()")
    # if not title:
    #     title = info.xpath("./div[@class='jItem']/div[@class='jGoodsInfo']/div[@class='jDesc']/a/text()")
    #
    #
    #
        item = {
            "href": href[0],
            "title": title[0],
        }
        if not href or not title:
            continue
        li.append(item)

print(li)
print(len(li))
with open(r"D:\code\block\xpath\txt\tianmao_oppo.txt", "w", encoding='utf-8') as f:
    for info in li:
        f.write(repr(info))
        f.write("\n")

