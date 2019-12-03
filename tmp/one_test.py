import logging
import platform
import time
import traceback

import requests

logger = logging

if 'Win' in platform.system():
    proxy_url = 'http://proxy.yuntingai.com/proxy/getProxy/29'
else:
    proxy_url = 'http://10.1.6.218/proxy/getProxy/29'


def get_proxy(retry_state):
    global proxies
    while True:
        url1 = proxy_url
        try:
            res = requests.get(url1, timeout=3)
            if res.status_code != 200:
                continue
            proxy_info = res.json()
            if proxy_info.get('trueIp'):
                if proxy_info['type'] == 'http':
                    proxy_info['type'] = 'http'
                else:
                    proxy_info['type'] = 'socks5'
                type_info = proxy_info['type']
                name = proxy_info['name']
                password = proxy_info['password']
                host = proxy_info['host']
                port = proxy_info['port']
                proxies = {
                    'https': "{}://{}:{}@{}:{}".format(type_info, name, password, host, port),
                    'http': "{}://{}:{}@{}:{}".format(type_info, name, password, host, port),
                }
                print(proxy_info.get('trueIp'))
                print(proxies)
                break
            else:
                logger.info("当前获取ip代理 没有真实ip")
                time.sleep(2)
                continue
        except Exception:
            logger.info(traceback.format_exc())
            time.sleep(3)


if __name__ == '__main__':
    get_proxy("1")
