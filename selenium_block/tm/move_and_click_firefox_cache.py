import math
import platform
import random
import time
import traceback

import requests
from scrapy.crawler import logger
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if 'Win' in platform.system():
    proxy_url = 'http://proxy.yuntingai.com/proxy/getProxy/999'
else:
    proxy_url = 'http://10.1.6.218/proxy/getProxy/999'


def get_proxy(retry_state):
    # global proxies
    while True:
        url1 = proxy_url
        try:
            res = requests.get(url1, timeout=5)
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
                    'username': name,
                    'password': password,
                    'host': host,
                    'port': port,
                }
                print("当前代理", proxies, "trueIp", proxy_info.get('trueIp'))
                return proxies
            else:
                print("当前获取ip代理 没有真实ip")
                time.sleep(2)
                continue
        except Exception:
            print(traceback.format_exc())
            time.sleep(3)


class Spider(object):
    def __init__(self, proxies=None, url="", cookie="", username="", password=""):
        self.cookie = cookie
        self.url = url
        self.proxies = proxies
        if proxies:
            self.ip_name = proxies['username']
            self.ip_pass = proxies['password']
            self.ip_host = proxies['host']
            self.ip_port = proxies['port']
        else:
            self.proxies = ""
        if "Win" in platform.system():
            executable_path = r'D:\code\block\selenium_block\tm\geckodriver.exe'
        else:
            executable_path = r'/root/gerapy/projects/scrapy_mall/scrapy_mall/until/geckodriver'

        self.driver = webdriver.Firefox(proxy=self._proxy(), firefox_profile=self._set_profile(),
                                        firefox_options=self._set_options(),
                                        executable_path=executable_path)
        self.wait = WebDriverWait(self.driver, 10)

        self.username = username
        self.password = password

    def _proxy(self):
        mimvp_proxy = {
            'ip': self.ip_host,  # ip
            # 'port_https': 19480,  # http, https
            'port_socks': self.ip_port,  # socks5
            'username': self.ip_name,
            'password': self.ip_pass
        }

        proxy_config = Proxy({
            'proxyType': ProxyType.MANUAL,  # 1
            'socksProxy': mimvp_proxy['ip'] + ":" + str(mimvp_proxy['port_socks']),
            'socksUsername': mimvp_proxy['username'],
            'socksPassword': mimvp_proxy['password'],
        })
        return proxy_config

    def _set_profile(self):
        profile = FirefoxProfile()
        # 激活手动代理配置（对应着在 profile（配置文件）中设置首选项）
        if self.proxies:
            profile.set_preference("network.proxy.type", 1)
            # ip及其端口号配置为 http 协议代理
            # profile.set_preference("network.proxy.http", self.ip)
            # profile.set_preference("network.proxy.http_port", int(self.port))
            # profile.set_preference('network.proxy.ssl', self.ip)
            # profile.set_preference('network.proxy.ssl_port', int(self.port))
            profile.set_preference("network.proxy.socks", self.ip_host)
            profile.set_preference("network.proxy.socks_port", int(self.ip_port))
            profile.set_preference("network.proxy.socks_version", 5)
            #
            profile.set_preference("network.proxy.socksUsername ", self.ip_name)  # TODO
            profile.set_preference("network.proxy.socksPassword ", self.ip_pass)  # TODO
            profile.update_preferences()
            # 所有协议共用一种 ip 及端口，如果单独配置，不必设置该项，因为其默认为 False
            # profile.set_preference("network.proxy.share_proxy_settings", True)
            pass

        # 默认本地地址（localhost）不使用代理，如果有些域名在访问时不想使用代理可以使用类似下面的参数设置
        # profile.set_preference("network.proxy.no_proxies_on", "localhost")
        return profile

    def _set_options(self):
        options = Options()
        options.add_argument('--window-size=1366,768')
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_argument('--headless')
        return options

    def move_button(self):
        try:
            self.driver.get("https://httpbin.org/get")
            time.sleep(2)
            # self.driver.delete_all_cookies()
            if self.cookie:
                self.driver.add_cookie(self.cookie)

            self.driver.get(self.url)

            time.sleep(1)
            self.driver.switch_to.frame("sufei-dialog-content")

            time.sleep(1)
            username_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TPL_username_1"]')))
            username_input.send_keys(self.username)

            time.sleep(1)
            password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TPL_password_1"]')))
            password_input.send_keys(self.password)
            slide_times = 0

            time.sleep(1)
            login_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="J_SubmitStatic"]')))
            login_input.click()

            time.sleep(1)
            while True:
                slide_times = slide_times + 1
                if slide_times > 5:
                    break
                try:
                    # self.driver.switch_to.frame("sufei-dialog-content")
                    pass
                except Exception:
                    print(traceback.format_exc())
                    pass

                # 如果刷新
                try:
                    button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@id="nc_1_n1z"]')))
                    time.sleep(random.randint(3, 5))
                    ActionChains(self.driver).click_and_hold(button).perform()
                    list = [258, 259, 260, 261, 262, 263, 264, 265, 266]
                    ActionChains(self.driver).move_by_offset(xoffset=random.choice(list), yoffset=0).perform()
                    ActionChains(self.driver).release().perform()

                    time.sleep(random.randint(1))
                    rset = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="nc-lang-cnt"]/a')))
                    time.sleep(random.randint(3, 5))
                    rset.click()
                    continue
                except Exception:
                    time.sleep(random.randint(3, 5))
                    break
        except Exception as e:
            time.sleep(random.randint(5, 5))
            logger.error(traceback.format_exc())

    def slide_move(self, position):
        # 移动位置的列表
        position_list = []
        for x in range(-5, 6):
            s1 = position / (1 + math.exp(-x))
            s2 = position / (1 + math.exp((-x - 1)))
            a = s2 - s1
            if int(a) == 0:
                a = 1
            else:
                a = int(a)
            position_list.append(a)
        return position_list

    def get_cookie(self):

        cookie = self.driver.get_cookies()
        new_cookie = {}
        for i in cookie:
            name = i['name']
            value = i['value']
            new_cookie[name] = value
            # if 'x5sec' in name:
            #     new_cookie[name] = value

        print("new_cookie: {}".format(new_cookie))
        return new_cookie

    def start(self, *args, **kwargs):
        try:
            self.move_button()
            cookies = self.get_cookie()
            cookie_str = ""
            for cookie in cookies:
                cookie_str = cookie_str + cookie + "=" + cookies[cookie] + ";"
            return cookie_str[:-1]
        except Exception as e:
            logger.error(e)
            return ""
        finally:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(e)


if __name__ == '__main__':
    url_one = "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F"
    username = "小卡_tb"
    password = "heweihua59"
    proxies_info = get_proxy(1)
    cookie = Spider(url=url_one, username=username, password=password, proxies=proxies_info).start()
    print(cookie)
