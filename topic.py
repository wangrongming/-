import requests

mall_name = "galanzqfy"
url = "https://{}.tmall.com/search.htm".format(mall_name)

querystring = {"orderType":"","viewType":"grid","keyword":"","lowPrice":"","highPrice":""}
headers = {
    'authority': "{}.tmall.com".format(mall_name),
    'cache-control': "max-age=0,no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    'sec-fetch-mode': "navigate",
    'sec-fetch-user': "?1",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'sec-fetch-site': "same-origin",
    'referer': "https://{}.tmall.com/?q=1&type=p&search=y&newHeader_b=s_from&searcy_type=item&from=.shop.pc_2_searchbutton&spm=a1z10.1-b.a2227oh.d101".format(mall_name),
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cookie': "cna=YOIqFqvLJS0CARsmIBhFiPPu; t=9bf1d58d5cb5205c17826fc461f9c747; enc=zASu8fjs%2B%2BH5sTxq6BE98Xe8TbAQQ1QQ8c9NdXQiulT7kRkUr6%2F9BNMokLyezPC%2BhMwZlS71yh30JEz3q7jyog%3D%3D; _tb_token_=78e91889e1815; cookie2=184acf32c6c3ff55612673fece8ac239; pnm_cku822=; cq=ccp%3D1; l=dBOYYnKVqZXiWD6yBOCiNuIRuFQOQIRAguPRwtGpi_5Bl1LsD37OkQ1_8ep6cjWfT7TB4cULngv9-etkiepTY-AS-zK6rxDc.; isg=BD4-QnvV7yyIQDsPs2O7Aiimj1RA12zMwRf2SehHtAF8i95lUA0hCMlpAxfis_oR",
    'Host': "{}.tmall.com".format(mall_name),
    'Connection': "keep-alive"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)