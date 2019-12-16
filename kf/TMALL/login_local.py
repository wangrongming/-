# encoding: utf-8
"""
@author: Liu
@file: login.py
@time: 2019/9/18 10:46 AM
"""
import os
import sys

sys.path.append(os.path.abspath("../.."))
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("."))
import asyncio
import random
import time
import logging.handlers
from pyppeteer import launch

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# f_handler = logging.handlers.TimedRotatingFileHandler(r'/root/send_cookie/log/pyppeteer_get_cookie.json',when='midnight', interval=1, backupCount=3)
# f_handler.setLevel(logging.INFO)
# logger.addHandler(f_handler)


async def login(username, password, url):
    try:
        # 'headless': False如果想要浏览器隐藏更改False为True
        browser = await launch(headless=False, userDataDir='.userdata', defaultViewport={'width': 1280, 'height': 800},
                               args=['--enable-automation', '--no-sandbox'])
        page = await browser.newPage()
        result = await taobao(username, password, url, page)
        if result:
            username, cookies = result
            await browser.close()
            return username, cookies
        else:
            await browser.close()
            return None
    except Exception as e:
        logger.exception(e)


async def taobao(username, password, url, page):
    """
    淘宝登录主程序
    :param username: 用户名
    :param password: 密码
    :param url: 登录网址
    :return: 登录cookies
    """
    await page.setViewport(viewport={'width': 1280, 'height': 800})
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36')
    await page.goto(url)
    print('page.go' + url)

    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    print('js加载完毕')
    time.sleep(2)
    try:
        await page.click('#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
    except Exception as e:
        print(e)
    # 输入用户名，密码
    await page.evaluate('''document.getElementById("TPL_username_1").value=""''')
    await page.type('#TPL_username_1', username, {'delay': input_time_random()})  # delay是限制输入的时间
    await page.type('#TPL_password_1', password, {'delay': input_time_random()})
    await asyncio.sleep(2)
    # 检测页面是否有滑块。原理是检测页面元素。
    try:
        print('是否有滑块')
        slider = await page.Jeval('#nocaptcha', 'node => node.style')
    except Exception as e:
        print('没有滑块')
        slider = None

    if slider:
        print('当前页面出现滑块')
        # await page.screenshot({'path': './headless-login-slide.png'}) # 截图测试
        flag, page = await mouse_slide(page=page)  # js拉动滑块过去。
        if flag:
            n = 0
            while n < 5:
                try:
                    await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')
                    break
                except Exception as e:
                    print('登录按钮问题')
                    n += 1
            result = await get_cookie(username, page, url)
            return result if result else None

    else:
        print('当前页面没有出现滑块，直接登录')
        await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')
        await page.waitFor(20)
        time.sleep(5)
        await page.waitForNavigation()

        try:
            global error  # 检测是否是账号密码错误
            print("error_1:", error)
            error = await page.Jeval('.error', 'node => node.textContent')
            print("error_2:", error)
        except Exception as e:
            error = None
        finally:
            if error:
                print('确保账户安全重新入输入')
            else:
                # await asyncio.sleep(2000)
                page = await go_kf_page(page)  # TODO
                result = await get_cookie(username, page, url)
                return result if result else None


async def go_kf_page(page):
    """
    访问子账号页面
    :param page:
    :return:
    """
    await page.goto(
        'https://zizhanghao.taobao.com/subaccount/monitor/chat_record_query.htm?spm=a211ki.11005426.a311j.2.5d0961c41j5NBK')
    return page


# 获取登录后cookie
async def get_cookie(username, page, url):
    await page.waitFor(2000)
    print('cookie页面的url' + page.url)
    print('cookie页面的url' + page.url)
    cookies_list = await page.cookies()
    cookies = {}
    for cookie in cookies_list:
        cookies[cookie['name']] = cookie['value']
    await page.screenshot({'path': 'zhangslob.png'})
    await page.close()
    return username, cookies


def retry_if_result_none(result):
    return result is None


async def mouse_slide(page=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1_n1z')  # 不同场景的验证码模块能名字不同。
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        logger.exception(e)
        return None, page
    else:
        await asyncio.sleep(2)
        print('判断是否通过')
        slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        if slider_again != '验证通过':
            print('验证滑块验证不通过')
            return None, page
        else:
            # await page.screenshot({'path': './headless-slide-result.png'}) # 截图测试
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)


def run(username, password, url):
    # display = Display(visible=0, size=(1920, 1080))
    # display.start()
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(login(username, password, url))
    loop.run_until_complete(task)
    cookie = task.result()

    old_cookie = cookie[1]
    COOKIE = ''
    for i in old_cookie:
        COOKIE += i + '=' + old_cookie[i] + ';'
    print(COOKIE)
    # display.stop()
    return cookie


if __name__ == '__main__':
    username = 'oppo官方旗舰店:羊羊'  # 百草味
    password = ''
    url = 'https://zizhanghao.taobao.com/subaccount/monitor/chat_record_query.htm?spm=a211ki.11005426.a311j.2.5d0961c41j5NBK'
    run(username, password, url)
