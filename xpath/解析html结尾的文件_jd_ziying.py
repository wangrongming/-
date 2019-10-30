from lxml import etree


info = etree.parse(r'D:\code\block\xpath\html\oppo_jd_ziying_all.html', etree.HTMLParser(encoding='utf-8'))
sel = info.xpath("//div[@class='jSearchListArea jCurrent']/div[@class='j-module jCurrent']/ul/li")
li = []
print(sel)
for info in sel:

    href = info.xpath("./div[@class='jItem jCurrent']/div[@class='jGoodsInfo']/div[@class='jDesc']/a/@href")
    title = info.xpath("./div[@class='jItem jCurrent']/div[@class='jGoodsInfo']/div[@class='jDesc']/a/text()")
    if not href:
        href = info.xpath("./div[@class='jItem']/div[@class='jGoodsInfo']/div[@class='jDesc']/a/@href")
        title = info.xpath("./div[@class='jItem']/div[@class='jGoodsInfo']/div[@class='jDesc']/a/text()")
    item = {
            "href": href[0],
            "title": title[0],
        }
    # if not href or not title:
    #     continue
    li.append(item)

print(li)
print(len(li))
with open(r"D:\code\block\xpath\txt\oppo_jd_ziying_all.txt", "a", encoding='utf-8') as f:
    for info in li:
        f.write(repr(info))
        f.write("\n")

