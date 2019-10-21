import requests

# curl -x "http://hty001:Hty8899@36.26.210.83:31281" httpbin.org/get
def set_proxy():
    while True:
        url1 = 'http://proxy.dataduoduo.com/proxy/getProxy?tid=999'
        try:
            res = requests.get(url1, timeout=3)
        except Exception:
            continue
        if res.status_code != 200:
            continue
        proxy_info = res.json()
        try:
            if proxy_info['isAlive']:
                if proxy_info['type'] == 'http':
                    proxy_info['type'] = 'http'
                else:
                    proxy_info['type'] = 'socks5'
                return {
                    'https': "{}://{}:{}@{}:{}".format(proxy_info['type'], proxy_info['userName'],
                                                       proxy_info['passWord'],
                                                       proxy_info['host'], proxy_info['port']),
                    'http': "{}://{}:{}@{}:{}".format(proxy_info['type'], proxy_info['userName'],
                                                      proxy_info['passWord'],
                                                      proxy_info['host'], proxy_info['port']),
                }
        except TypeError:
            pass

