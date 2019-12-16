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
    "Cookie": "BAIDUID=605814558314225655B02F4A7CD0727A:FG=1; BIDUPSID=605814558314225655B02F4A7CD0727A; PSTM=1571018906; H_PS_PSSID=1467_21112_30210_18560; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=vA8sJeCCxG3eBBrwnPk1ehPAL8CH6AQX2liC3J; H_BDCLCKID_SF=tbkD_C-MfIvhDRTvhCcjh-FSMgTBKI62aKDsLqDy-hcqEpO9QTbqLxDX5UTTa5o-2NRC2InnWIQNVfP4h-rTDUTh-p52f60efnPD3J; delPer=0; PSINO=6; BDUSS=kVya0F-cTV3RWp3SkM5c2dpY3dyMUJLckExRnpVT0tiVjctdkJKckM2NGZ-eDVlSVFBQUFBJCQAAAAAAAAAAAEAAABIvZ0nx-zD92hhcHB5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB9y910fcvddb; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1576497490,1576497705; bdindexid=iaaltnapiblph156e6561b5436; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1576497713",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.142 Safari/537.36"
}

data_url = 'https://index.baidu.com/api/SearchApi/index?word={}&area=0&days=7'
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
