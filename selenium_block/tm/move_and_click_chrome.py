import json
import math
import platform
import random
import re
import time
import traceback

from scrapy.crawler import logger
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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
            executable_path = r'D:\code\block\selenium_block\tm\chromedriver.exe'
        else:
            executable_path = r'/root/gerapy/projects/scrapy_mall/scrapy_mall/until/geckodriver'
        self.driver = webdriver.Chrome(chrome_options=self._set_options(),
                                       executable_path=executable_path)
        self.wait = WebDriverWait(self.driver, 10)

    def _set_options(self):
        options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--window-size=1366,768')
        # options.add_argument('--headless')
        if 'Win' not in str(platform.architecture()):
            options.add_argument('--no-sandbox')

        # try:
        #     options.add_argument("--proxy-server=%s" % "http://" + str(self.proxies))
        # except:
        #     options.add_argument("--proxy-server=%s" % "http://" + str(self.proxies))
        return options

    def move_button(self):
        try:
            # self.driver.get("https://httpbin.org/get")
            time.sleep(2)
            self.driver.delete_all_cookies()
            if self.cookie:
                self.driver.add_cookie(self.cookie)

            self.driver.get(self.url)
            time.sleep(1)

            js1 = '''Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) '''

            js2 = '''window.navigator.chrome = { runtime: {},  }; '''

            js3 = '''Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); '''

            js4 = '''Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); '''

            self.driver.execute_script(js1)

            self.driver.execute_script(js2)

            self.driver.execute_script(js3)

            self.driver.execute_script(js4)

            time.sleep(1)
            self.driver.switch_to.frame("sufei-dialog-content")

            time.sleep(1)
            username = "小卡_tb"
            password = "heweihua59"
            username_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TPL_username_1"]')))
            username_input.send_keys(username)

            time.sleep(1)
            password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TPL_password_1"]')))
            password_input.send_keys(password)
            slide_times = 0

            slide_times = 0
            while True:
                slide_times = slide_times + 1
                if slide_times > 2:
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

                    rset = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="nc-lang-cnt"]/a')))
                    time.sleep(random.randint(3, 5))
                    rset.click()
                    continue
                except Exception:
                    time.sleep(random.randint(3, 5))
                    break

            time.sleep(1)
            login_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="J_SubmitStatic"]')))
            login_input.click()
            
        except Exception as e:
            time.sleep(random.randint(5, 5))
            logger.error(e)

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

            if 'x5sec' in name:
                new_cookie[name] = value
            if 'key' in name:
                new_cookie[name] = value
            if 'guid' in name:
                new_cookie[name] = value
            if 'UM_distinctid' in name:
                new_cookie[name] = value
            if 'cna' in name:
                new_cookie[name] = value
            if 'CNZZDATA' in name:
                new_cookie[name] = value
            if 'isg' in name:
                new_cookie[name] = value

        logger.info("new_cookie: {}".format(new_cookie))
        return new_cookie

    def get_headers(self, browser):
        for responseReceived in browser.get_log('performance'):
            try:
                response = json.loads(responseReceived[u'message'])[u'message'][u'params'][u'response']
                if response[u'url'] == browser.current_url:
                    return response[u'headers']
            except:
                pass
        return None

    def start(self, *args, **kwargs):
        try:
            self.move_button()
            print(self.get_headers(self.driver))
            cookies = self.get_cookie()
            return cookies
        except Exception as e:
            logger.error(e)
            return ""
        finally:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(e)


if __name__ == '__main__':
    url_one = "https://baicaowei.m.tmall.com/shop/shop_auction_search.htm?spm=a2141.7631565.0.0.59563928MSrl65&suid=628189716&sort=default"
    Spider(url=url_one).start()
