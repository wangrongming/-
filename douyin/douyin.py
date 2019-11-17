import requests


def one():
    headers = {
        'Host': 'aweme-eagle-hl.snssdk.com',
        'Connection': 'keep-alive',
        'Cookie': 'install_id=68314548134; ttreq=1$0307e2790187f343249b26a8fbe1e34c70666b0a; odin_tt=e01c8b5a0cf6c8b5a2a60c21d1e7c9886e45c960d708ffd2913c2f28894d2e677033a22a2a5fa2e541e740f21a7e37224188e56101774d752d02ead33ef33315; uid_tt=e7565ff11c4ef0ef070f1c4e9cbc5cb6; sid_tt=0b587d031c02f8497bf2e6b413dad995; sessionid=0b587d031c02f8497bf2e6b413dad995; sid_guard=0b587d031c02f8497bf2e6b413dad995%7C1572100633%7C5184000%7CWed%2C+25-Dec-2019+14%3A37%3A13+GMT; qh[360]=1',
        'Accept-Encoding': 'gzip',
        'X-SS-REQ-TICKET': '1573996904563',
        'X-Tt-Token': '000b587d031c02f8497bf2e6b413dad995bc6191f573fd9f09131f2933b23d069fbbb8c01057adbaeb9393529e5d06c1e630',
        'sdk-version': '1',
        'User-Agent': 'com.ss.android.ugc.aweme/551 (Linux; U; Android 9; zh_CN; MI 8; Build/PKQ1.180729.001; Cronet/58.0.2991.0)',
        'X-Khronos': '1573996904',
        'X-Gorgon': '03006cc00000859def42a76ab91ca419aa3a9c1f032cbb28f34c',
        'X-Pods': '',
    }
    url = "https://aweme-eagle-hl.snssdk.com/aweme/v1/user/?user_id=81939158402&retry_type=no_retry&mcc_mnc=46000&iid=68314548134&device_id=57999941945&ac=wifi&channel=xiaomi&aid=1128&app_name=aweme&version_code=551&version_name=5.5.1&device_platform=android&ssmix=a&device_type=MI+8&device_brand=Xiaomi&language=zh&os_api=28&os_version=9&openudid=930d69eabc40515f&manifest_version_code=551&resolution=1080*2029&dpi=440&update_version_code=5512&_rticket=1573996904557&ts=1573996904&js_sdk_version=1.13.10&as=a185c45db856ed99416744&cp=4a69d05f8418d19ee1Sg%5Bk&mas=0113e5f7bfcf8ee8d289a893744fa3abe12c2cec6c8c2c9c9c26a6"
    res = requests.get(url=url, headers=headers)
    print(res.text)


if __name__ == '__main__':
    one()
