import logging
import platform
import random
import re
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if "Win" in platform.system():
    logging.basicConfig(level=logging.INFO)


class Spider(object):
    def __init__(self, proxies="", url="", cookie=""):
        self.cookie = cookie
        self.url = url
        if proxies:
            self.proxies = proxies
            self.ip = re.split(":", self.proxies)[0]
            self.port = re.split(":", self.proxies)[1]
        else:
            self.proxies = ""
        if "Win" in platform.system():
            executable_path = r'D:\block\selenium_block\geckodriver.exe'
        else:
            executable_path = r'/root/gerapy/projects/scrapy_mall/scrapy_mall/until/geckodriver'
        self.driver = webdriver.Firefox(firefox_options=self._set_options(),
                                        executable_path=executable_path)
        self.wait = WebDriverWait(self.driver, 10)

    def _set_profile(self):
        profile = FirefoxProfile()
        # 激活手动代理配置（对应着在 profile（配置文件）中设置首选项）
        if self.proxies:
            profile.set_preference("network.proxy.type", 1)
            # ip及其端口号配置为 http 协议代理
            profile.set_preference("network.proxy.http", self.ip)
            profile.set_preference("network.proxy.http_port", int(self.port))
            profile.set_preference('network.proxy.ssl', self.ip)
            profile.set_preference('network.proxy.ssl_port', int(self.port))
            profile.set_preference("network.proxy.username", 'aaaaa')  # TODO
            profile.set_preference("network.proxy.password", 'bbbbb')  # TODO
            profile.update_preferences()
            # 所有协议共用一种 ip 及端口，如果单独配置，不必设置该项，因为其默认为 False
            profile.set_preference("network.proxy.share_proxy_settings", True)

        # 默认本地地址（localhost）不使用代理，如果有些域名在访问时不想使用代理可以使用类似下面的参数设置
        # profile.set_preference("network.proxy.no_proxies_on", "localhost")
        return profile

    def _set_options(self):
        options = Options()
        options.add_argument('--window-size=1366,768')
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_argument('--headless')
        return options

    def exec_js(self):
        # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
        try:
            self.driver.execute_script(
                '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
            self.driver.execute_script('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
            self.driver.execute_script(
                '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
            self.driver.execute_script(
                '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

            logging.info('js加载完毕')
        except Exception as e:
            logging.exception("js加载异常 {}".format(e))

    def move_button(self):
        try:
            slide_times = 0
            while True:
                self.exec_js()
                slide_times = slide_times + 1
                if slide_times > 5:
                    break

                # 如果刷新
                try:
                    button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@id="nc_1_n1z"]')))
                    time.sleep(random.randint(3, 5))
                    ActionChains(self.driver).click_and_hold(button).perform()
                    list = [258, 259, 260, 261, 262, 263, 264, 265, 266]
                    ActionChains(self.driver).move_by_offset(xoffset=random.choice(list), yoffset=0).perform()
                    ActionChains(self.driver).release().perform()

                    rset = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="nc-lang-cnt"]/a')))
                    time.sleep(random.randint(3, 5))
                    rset.click()
                    logging.error(f"滑动失败重试 {slide_times} 次")
                    continue
                except Exception as e:
                    logging.error(e)
                    logging.info("滑块滑动成功")
                    time.sleep(random.randint(3, 5))
                    return True
        except Exception as e:
            time.sleep(random.randint(5, 5))
            logging.exception(e)
            return False

    def login(self):
        self.driver.get("https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F")
        user_name = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TPL_username_1"]')))
        time.sleep(1)
        user_name.send_keys("wangrongmingtaobao")

        pass_word = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TPL_password_1"]')))
        time.sleep(1)
        pass_word.send_keys("zm1768389896xwmt")

        submit = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_SubmitStatic"]')))
        time.sleep(1)
        submit.click()
        pass

    def crawler_page(self):
        for i in range(2, 6):
            time.sleep(5)
            url = f"https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.9.67d039360ach8L&cat=50106425&s={(i-1)*60}&oq=%C9%CC%B3%A1%CD%AC%BF%EE&sort=s&style=g&vmarket=35458&from=sn_1_cat&active=1&industryCatId=50106425&type=pc#J_Filter"
            self.driver.get(url)
            text = self.driver.page_source

            if "J_SubmitStatic" in text:
                self.login()

            if "小二正忙，滑动一下马上回" in text:
                print(f"采集{i}页 出现滑块")
                res = self.move_button()
                if res:
                    print("正常采集 {}页".format(i))
                    continue
                else:
                    print("滑动失败，采集终止 采集 {}页".format(i))
                    break
            print("正常采集 {}页".format(i))

    def start(self, *args, **kwargs):
        try:
            # self.login()
            self.crawler_page()
        except Exception as e:
            logging.exception(e)
            return ""
        finally:
            try:
                time.sleep(5)
                self.driver.quit()
            except Exception as e:
                logging.exception(e)


if __name__ == '__main__':
    url_one = "https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F"
    Spider(url=url_one).start()
