import datetime
import json
import platform

import requests
import tenacity


class NetworkProxy:

    @classmethod
    @tenacity.retry(reraise=True, stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_random(min=2, max=5))
    def _get_proxy(cls, url: str):
        try:
            res = requests.get(url, timeout=10)
        except Exception:
            raise Exception(f"无法成功获取代理 {url}")

        if 'Win' in platform.system():

            proxy_json = json.loads(res.text, encoding="utf-8")
            true_ip = proxy_json.get("trueIp")
            if true_ip is None or "" == true_ip:
                raise Exception(f"代理不可用 {res.text}")
            return {
                "type": proxy_json['type'] + "5",
                "username": proxy_json.get('name', ""),
                "password": proxy_json.get('password', ""),
                "host": proxy_json.get('host', ""),
                "port": proxy_json.get('port', "")
            }

        else:
            # proxy_url = "http://10.1.1.97:8086/proxy/getProxy?tid=299&mode=socks"
            # {"id":4638,"line":2,"host":"175.6.247.162","port":20008,"startTime":"2020-05-16 21:38:08","isAlive":true,
            # "type":"socks","userName":"BZYZ018684T","passWord":"6215"}

            proxy_json = json.loads(res.text)
            true_ip = proxy_json.get("trueIp", False)
            is_alive = proxy_json.get("isAlive", False)
            if not true_ip and not is_alive:
                raise Exception(f"无trueIp/isAlive=False，代理不可用 {res.text}")

            start_time = proxy_json.get('startTime', None)
            if start_time:
                str_timestamp = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').timestamp()
                now_timestamp = datetime.datetime.now().timestamp()
                # if now_timestamp - str_timestamp > 600:
                #     raise Exception(f"代理存在超过10min 代理不可用 {res.text}")
            if proxy_json['type'] == "http":
                proxy_type = proxy_json['type']
            else:
                proxy_type = proxy_json['type'] + "5"
            return {
                "type": proxy_type,
                "username": proxy_json.get('userName', ""),
                "password": proxy_json.get('passWord', ""),
                "host": proxy_json.get('host', ""),
                "port": proxy_json.get('port', "")
            }

    @classmethod
    def get_proxy(cls, plat_info, task_type=None):
        # 代理获取地址
        if 'Win' in platform.system():
            proxy_url = "http://price.proxy.yuntingai.com/proxy/getProxy/999"  # 999
        else:
            # tmall的价格  淘宝的价格 jd的评论 用阿布云代理 其他请求使用uuhttp
            if task_type in ["TMALL_SPU_PROMOTION", "JD_SKU_COMMENT"]:  # TODO 待补全
                # 阿布云代理
                proxy_url = "http://10.1.1.97:8086/proxy/getProxy?tid=299&mode=socks"
            else:
                # uuhttp
                proxy_url = "http://10.1.6.120:30005/proxy/getProxy/{}"
                dt = {
                    "tmall": "101",
                    "jd": "102",
                    "suning": "103",
                    "taobao": "104",
                }
                code = dt.get(plat_info, "101")
                proxy_url = proxy_url.format(code)

        proxy = cls._get_proxy(proxy_url)
        log_info = {"plat_info": plat_info, "task_type": task_type, **proxy, "proxy_url": proxy_url}
        print("获取代理", log_info)
        if proxy.get("username") and proxy.get("password"):
            proxy_url = '{type}://{username}:{password}@{host}:{port}'.format(**proxy)
        else:
            proxy_url = '{type}://{host}:{port}'.format(**proxy)
        return {'http': proxy_url, 'https': proxy_url}


if __name__ == '__main__':
    info = NetworkProxy.get_proxy("", task_type="TMALL_SPU_PROMOTION")
    # info = NetworkProxy.get_proxy("", task_type="")
    print(info)
