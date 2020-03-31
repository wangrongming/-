import logging
import platform
import random
import re
import time
import traceback

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
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
            executable_path = r'D:\code\block\selenium_block\chromedriver.exe'
        else:
            executable_path = r'/root/gerapy/projects/scrapy_mall/scrapy_mall/until/geckodriver'
        self.driver = webdriver.Chrome(chrome_options=self._set_options(),
                                       executable_path=executable_path)
        self.wait = WebDriverWait(self.driver, 10)

    def _set_options(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
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
            while True:
                slide_times = slide_times + 1
                if slide_times > 2:
                    break
                try:
                    self.driver.switch_to.frame("sufei-dialog-content")
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
        except Exception as e:
            time.sleep(random.randint(5, 5))
            logging.exception(e)

    def login(self):
        self.driver.get("https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F")
        user_name = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TPL_username_1"]')))
        time.sleep(1)
        user_name.send_keys("小卡_tb")

        pass_word = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TPL_password_1"]')))
        time.sleep(1)
        pass_word.send_keys("heweihua59")

        submit = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_SubmitStatic"]')))
        time.sleep(1)
        submit.click()
        pass

    def crawler_page(self):
        url = "https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.9.2b4ea64aDE7Ajq&s=60&q=%B1%F9%E4" \
              "%BF%C1%DC&sort=s&style=g&from=.list.pc_1_searchbutton&active=1&type=pc#J_Filter "
        self.driver.get(url)
        text = self.driver.page_source

        if "J_SubmitStatic" in text:
            self.login()

        if "小二正忙，滑动一下马上回" in text:
            print("出现滑块")
            self.move_button()
            return

        print("正常采集")
        return

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
