import json
import platform

import requests
import tenacity


class ProxyGetException(Exception):
    pass


class ProxyRequestException(Exception):
    pass


class DataProxy:
    if 'Win' in platform.system():
        PROXY_COMMENT_URL = "http://proxy.yuntingai.com/proxy/getProxy/{}"

        PROXY_PRICE_URL = "http://price.proxy.yuntingai.com/proxy/getProxy/{}"
    else:
        PROXY_COMMENT_URL = "http://10.1.6.218/proxy/getProxy/{}"

        PROXY_PRICE_URL = "http://10.1.6.137/proxy/getProxy/{}"

        # PROXY_COMMENT_URL = "http://proxy.yuntingai.com/proxy/getProxy/{}"
        #
        # PROXY_PRICE_URL = "http://price.proxy.yuntingai.com/proxy/getProxy/{}"

    @staticmethod
    @tenacity.retry(stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_random(min=1, max=5))
    def get_proxy(url: str, source_id: str):
        try:
            res = requests.get(url.format(source_id), timeout=5)
        except Exception:
            print("error")
            raise ProxyRequestException()

        proxy_json = json.loads(res.text)
        true_ip = proxy_json.get("trueIp")
        if true_ip is None or "" == true_ip:
            raise ProxyGetException()
        proxy_url = '{type}://{username}:{password}@{host}:{port}'.format(
            type=proxy_json['type'] + "5",
            username=proxy_json['name'],
            password=proxy_json['password'],
            host=proxy_json['host'],
            port=proxy_json['port']
        )
        return {'http': proxy_url, 'https': proxy_url}

    @staticmethod
    def get_index_proxy(source_id: str):
        return DataProxy.get_proxy(DataProxy.PROXY_PRICE_URL, source_id)


if __name__ == '__main__':
    print(DataProxy.get_index_proxy(source_id="19"))
