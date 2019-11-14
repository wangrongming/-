import requests

url = "https://weixin.sogou.com/weixin"

querystring = {"type":"2","s_from":"input","query":"%E5%B0%8F%E7%B1%B3","ie":"utf8","_sug_":"y","_sug_type_":"","w":"01019900","sut":"8769","sst0":"1573639082186","lkt":"0%2C0%2C0"}

headers = {
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    'Sec-Fetch-Mode': "navigate",
    'Sec-Fetch-User': "?1",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Sec-Fetch-Site': "same-origin",
    'Referer': "https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E5%B0%8F%E7%B1%B3&ie=utf8&_sug_=n&_sug_type_=",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cookie': "sct=1; SUV=0048174C1B2620395DCBD3AAEBE68538; ABTEST=5|1573639082|v1; IPLOC=CN4403; SUID=05B10FB74942910A000000005DCBD3AA",
    'Cache-Control': "no-cache",
    'Postman-Token': "abaed291-1398-47d0-8278-154e38c774a5,90866eca-a260-4511-92c2-841c0fbbee37",
    'Host': "weixin.sogou.com",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)