import time

import requests
from lxml import etree


def one():
    url = "http://tieba.baidu.com/f"

    # querystring = {"kw":"%E5%B0%8F%E7%B1%B3","ie":"utf-8","pn":"0"}
    querystring = {"kw":"%E5%B0%8F%E7%B1%B3","ie":"utf-8","pn":"50"}

    headers = {
        'Connection': "keep-alive",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cookie': "BAIDUID=605814558314225655B02F4A7CD0727A:FG=1; BIDUPSID=605814558314225655B02F4A7CD0727A; PSTM=1571018906; TIEBAUID=e624cd11040b60fb9b3b781a; TIEBA_USERTYPE=628f5f1020112c4945750e63; bdshare_firstime=1571041299685; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1467_21112_18560_29567_29699_29220; wise_device=0; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1573001604,1573002130,1573009550,1573009672; BDSFRCVID=Dk-OJeCinGA4cFTwkZJitB6YteKK0goTH6hK_yz1cxZNeuaxdimtEG0PHx8g0Ku-S2-AogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRAOoC8XfCvjDb7GbKTD-tFO5eT22-us3I0L2hcH0bT_spDm-Ujx5PPlyxrJ3j5kbITiaKJjaMb1MRnoBnr0DttbW4T--4oO5I5LLp5TtUJ1JKnTDMRhqqJXqtQyKMnitKv9-pP2LpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKu-n5jHjJLDG-D3D; delPer=0; PSINO=6; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948={}".format(int(time.time())),
        'Cache-Control': "no-cache",
        'Host': "tieba.baidu.com",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    html = response.text.replace('<!--', '').replace('-->', '')
    sel = etree.HTML(html)
    selector = sel.xpath("//*[@id='thread_list']/li")
    print(len(selector))
    print(html)
    print(len(selector))

def two():

    url = "http://tieba.baidu.com/f"

    querystring = {"kw":"%E5%B0%8F%E7%B1%B3","ie":"utf-8","pn":"0"}

    headers = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cookie': "BAIDUID=605814558314225655B02F4A7CD0727A:FG=1; BIDUPSID=605814558314225655B02F4A7CD0727A; PSTM=1571018906; TIEBAUID=e624cd11040b60fb9b3b781a; TIEBA_USERTYPE=628f5f1020112c4945750e63; bdshare_firstime=1571041299685; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1467_21112_18560_29567_29699_29220; wise_device=0; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1573001604,1573002130,1573009550,1573009672; BDSFRCVID=Dk-OJeCinGA4cFTwkZJitB6YteKK0goTH6hK_yz1cxZNeuaxdimtEG0PHx8g0Ku-S2-AogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRAOoC8XfCvjDb7GbKTD-tFO5eT22-us3I0L2hcH0bT_spDm-Ujx5PPlyxrJ3j5kbITiaKJjaMb1MRnoBnr0DttbW4T--4oO5I5LLp5TtUJ1JKnTDMRhqqJXqtQyKMnitKv9-pP2LpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKu-n5jHjJLDG-D3D; delPer=0; PSINO=6; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1573111493",
        'Postman-Token': "1fe82088-8d6b-4949-9895-d2b20b6d0283,c61afcce-0cc5-42b6-bff0-fee605a4393f",
        'Host': "tieba.baidu.com",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    html = response.text
    sel = etree.HTML(html)
    selector = sel.xpath("//*[@id='thread_list']/li")
    print(len(selector))
    print(html)
    print(len(selector))

if __name__ == '__main__':
    # one()
    two()