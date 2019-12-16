import time

from selenium import webdriver

from utils.cookie_utils import CookieUtils
from utils.yunting_proxy import YuntingProxy


def get_proxy(*args):
    global PROXY
    while True:
        PROXY = None
        try:
            PROXY = YuntingProxy.get_comment_proxy(source_id="3")
        except Exception as proxy_exception:
            print("{}：获取代理异常！exception_str：{}，line：{}".format(__file__, proxy_exception.__str__(), proxy_exception.__traceback__.tb_lineno))
            time.sleep(10)
        if PROXY is not None:
            break


class TmallShopCookieSpider:
    @staticmethod
    def init_proxy():
        get_proxy()

    @staticmethod
    def get_proxy():
        return PROXY

    @staticmethod
    def get_shop_cookie():
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("user-data-dir=userdata")
        # options.add_extension("d://proxy.zip")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        browser = webdriver.Chrome(executable_path="E:\\chromedriver_win32\\chromedriver.exe", options=options)
        browser.get("https://baicaowei.m.tmall.com/shop/shop_auction_search.htm?spm=a2141.7631565.0.0.59563928MSrl65&suid=628189716&sort=default")

        # browser.get("https://login.taobao.com")

        js1 = '''Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) '''

        js2 = '''window.navigator.chrome = { runtime: {},  }; '''

        js3 = '''Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); '''

        js4 = '''Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); '''

        browser.execute_script(js1)

        browser.execute_script(js2)

        browser.execute_script(js3)

        browser.execute_script(js4)

        time.sleep(100)

        print("等待完成！")

        # 如果有登录框，先登录，tmall提示喝水会有滑块
        # try:
        #     try:
        #         browser.switch_to.frame(browser.find_element_by_id("sufei-dialog-content"))
        #         try:
        #             username_input = browser.find_element_by_id("TPL_username_1")
        #             password_input = browser.find_element_by_id("TPL_password_1")
        #             print(username_input)
        #             print(password_input)
        #             username = "tb_小卡"
        #             password = "heweihua59"
        #             for i in range(len(username)):
        #                 username_input.send_keys(username[i:i + 1])
        #                 time.sleep(random.random())
        #
        #             for i in range(len(password)):
        #                 password_input.send_keys(password[i:i + 1])
        #                 time.sleep(random.random())
        #         except Exception as username_password_exception:
        #             print(f"{__file__}：未发现用户名密码输入框！exception_str：{username_password_exception.__str__()}，line：{username_password_exception.__traceback__.tb_lineno}")
        #
        #         try:
        #             slider = browser.find_element_by_id("nc_1_n1z")
        #             action_chains = webdriver.ActionChains(browser)
        #             action_chains.click_and_hold(slider).perform()
        #             action_chains.reset_actions()
        #
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(20, 0).perform()
        #             action_chains.move_by_offset(20, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(50, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(50, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(10, 0).perform()
        #             action_chains.move_by_offset(40, 0).perform()
        #         except Exception as slider_exception:
        #             print(f"{__file__}：未出现滑块！exception_str：{slider_exception.__str__()}，line：{slider_exception.__traceback__.tb_lineno}")
        #     except Exception as frame_exception:
        #         print(f"{__file__}：未出现弹出框！exception_str：{frame_exception.__str__()}，line：{frame_exception.__traceback__.tb_lineno}")
        #
        # except Exception as exception:
        #     print(f"{__file__}：出现异常！exception_str：{exception.__str__()}，line：{exception.__traceback__.tb_lineno}")
        #     pass

        cookie_dic = dict()
        cookie_list = browser.get_cookies()
        for cookie_item in cookie_list:
            cookie_dic[cookie_item["name"]] = cookie_item["value"]
        cookie_str = CookieUtils.parse_to_cookie_str(cookie_dic)
        cookie_str = cookie_str[0:len(cookie_str) - 1]
        print(cookie_str)

        # time.sleep(300)
        browser.quit()
        return cookie_str


if __name__ == '__main__':
    TmallShopCookieSpider.get_shop_cookie()
