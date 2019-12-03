# -*- coding: utf-8 -*-

import execjs
import requests
import urllib3

# 禁用警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

js_string = '''
function decrypt(t, e) {
    for (var n = t.split(""), i = e.split(""), a = {}, r = [], o = 0; o < n.length / 2; o++)
        a[n[o]] = n[n.length / 2 + o];
    for (var s = 0; s < e.length; s++)
        r.push(a[i[s]]);
    return r.join("")
}
'''

headers = {
    "Cookie": "BAIDUID=605814558314225655B02F4A7CD0727A:FG=1; BIDUPSID=605814558314225655B02F4A7CD0727A; PSTM=1571018906; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1467_21112_18560_29567_29699_29220; yjs_js_security_passport=886b4ad9441afd9c09ed281d9c94c276c2e4e043_1574755376_js; delPer=0; PSINO=6; ZD_ENTRY=baidu; BDSFRCVID=6s-sJeCCxG3JggRwYoqA0s8mW0FOeQZRddMu3J; H_BDCLCKID_SF=tR30WJbHMTrDHJTg5DTjhPrMjl-LbMT-027OKKOF5b3CfUTvKfL2KTkD3N3lW-QIyHrb0p6athF0HPonHjDKjTv03J; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1574821613,1574821648; BDUSS=m92U3pPNHR6UFhXU3pGS2RES3cxVjV6OWtBaGMwVzNkeDMzZHJRZHVWUFBiQVZlSVFBQUFBJCQAAAAAAAAAAAEAAADtRffWxa7A79esx64zMzk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM~f3V3P391db; CHKFORREG=4634288db9e03c542327bc830b7eaede; bdindexid=cmoeiomhafoio4rp5m2797r662; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1574827215",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.142 Safari/537.36"
}

# data_url = 'https://index.baidu.com/api/SearchApi/index?word={}&area=0&days=30'
data_url = 'http://index.baidu.com/api/SearchApi/index?area=0&word=%E5%A4%A7%E6%A0%91&startDate=2011-01-01&endDate=2011-12-31'
uniq_id_url = 'https://index.baidu.com/Interface/ptbk?uniqid={}'
keys = ["all", "pc", "wise"]


class BDIndex(object):

    def __init__(self):
        self.session = self.get_session()
        pass

    @staticmethod
    def get_session():
        """
            初始化 session 会话
        :return:
        """
        session = requests.session()
        session.headers = headers
        session.verify = False
        return session

    @staticmethod
    def decrypt(key, data):
        """
            得到解密后的数据
        :param key:  key
        :param data: key 对应的 value
        :return:
        """
        js_handler = execjs.compile(js_string)
        return js_handler.call('decrypt', key, data)

    def get_bd_index(self, key_word):
        """
            得到百度指数
        :param key_word:
        :return:
        """
        response = self.session.get(data_url.format(key_word)).json()
        uniq_id = self.session.get(
            uniq_id_url.format(response.get("data").get("uniqid"))
        ).json().get("data")

        result = []
        data_dict = response.get("data").get("userIndexes")[0]
        for key in keys:
            decrypt_data = self.decrypt(uniq_id, data_dict.get(key).get("data"))
            result.append({key: decrypt_data})
        return result


if __name__ == '__main__':
    bd = BDIndex()
    d = bd.get_bd_index("小米")
    print(d)
