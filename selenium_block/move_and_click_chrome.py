import platform
import random
import re
import time
import traceback

from PIL import Image
from scrapy.crawler import logger
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_block.chaojiying import Chaojiying_Client


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
            executable_path = r'D:\block\selenium_block\chromedriver_base.exe'
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
            self.driver.get("https://httpbin.org/get")
            time.sleep(2)
            self.driver.delete_all_cookies()
            if self.cookie:
                self.driver.add_cookie(self.cookie)

            self.driver.get(self.url)
            self.driver.refresh()
            slide_times = 0
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
            logger.error(e)

    def login(self):
        self.driver.get(self.url)

        code_input = self.save_image()

        code = self.img_to_code()
        code_input.send_keys(code['pic_str'])

        user_name = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        pass_word = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        submit = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="login-div login-div-btn"]')))
        time.sleep(1)
        user_name.send_keys("nsmsaadmin")
        time.sleep(1)
        pass_word.send_keys("NSmsa123")
        time.sleep(1)
        submit.click()
        pass

    def save_image(self):
        code_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="yzm"]')))
        code_input.click()

        time.sleep(1)
        self.driver.save_screenshot('print_screen.png')
        img_element = self.driver.find_element_by_id('certificationCodeImg')  # 定位验证码
        location = img_element.location  # 获取验证码x,y轴坐标
        print(location)
        size = img_element.size  # 获取验证码的长宽
        print(size)
        rangle = (int(location['x']),
                  int(location['y']),
                  int(location['x'] + size['width']),
                  int(location['y'] + size['height'])
                  )  # 写成我们需要截取的位置坐标
        i = Image.open("print_screen.png")  # 打开截图
        frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
        frame4 = frame4.convert('RGB')
        frame4.save('code.jpg')  # 保存我们接下来的验证码图片 进行打码
        return code_input

    def get_cookie(self):

        cookie = self.driver.get_cookies()
        new_cookie = {}
        for i in cookie:
            name = i['name']
            value = i['value']
            new_cookie[name] = value
        return new_cookie

    def img_to_code(self):
        chaojiying = Chaojiying_Client('wangwang', 'bao12345',
                                       '13a8c2ecd407f37e8f092d695bb46a15')
        # chaojiying = Chaojiying_Client('超级鹰用户名', '超级鹰用户名的密码', '96001')  # 用户中心>>软件ID 生成一个替换 96001
        im = open('code.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        return chaojiying.PostPic(im, 1902)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

    def start(self, *args, **kwargs):
        try:
            self.login()
            cookies = self.get_cookie()
            return cookies
        except Exception as e:
            logger.error(traceback.format_exc())
            return ""
        finally:
            try:
                time.sleep(5)
                self.driver.quit()
            except Exception as e:
                logger.error(e)


if __name__ == '__main__':
    url_one = "http://cas.szvsc.com/cas/login?flag=cmport&service=http%3A%2F%2Fwww.szvsc.com%2F#"
    cookie = Spider(url=url_one).start()
    print(cookie)
