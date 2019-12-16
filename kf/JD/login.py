import os
import sys

sys.path.append(os.path.abspath("../.."))
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("."))
import asyncio
import random
import time
import re
import numpy as np
from pyppeteer import launch
from PIL import Image
from io import BytesIO
import base64
from pymongo import MongoClient
from data_tool.setting import MONGO_HOST, MONGO_PORT, headless

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)


# db =client.get_database('kf_cookie')
# collection = db.get_collection('cookie')
# code_db = client.get_database('TCL_PHONE_CODE')
# code_collection = code_db.get_collection('code')

# 三个模拟轨迹的算法

def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)


def ease_out_quart(x):
    return 1 - pow(1 - x, 4)


def ease_out_expo(x):
    if x == 1:
        return 1
    else:
        return 1 - pow(2, -10 * x)


async def get_tracks(distance, seconds, ease_func):
    """
    获取移动的轨迹
    :param distance:路径长度
    :param seconds: 所消耗时间
    :param ease_func: 所使用的算法
    :return: 移动轨迹
    """
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        ease = globals()[ease_func]
        offset = round(ease(t / seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    return offsets, tracks


async def creat_browser():
    browser = await launch(headless=headless, userDataDir='.userdata', defaultViewport={'width': 1280, 'height': 800},
                           args=['--enable-automation', '--no-sandbox'])
    page = await browser.newPage()
    await page.setViewport(viewport={'width': 1280, 'height': 800})
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36')
    return (browser, page)


async def close_browser(browser):
    await browser.close()


async def login(page, username, password, url):
    try:
        # 'headless': False如果想要浏览器隐藏更改False为True
        # browser = await launch({'headless': False, 'args': ['--no-sandbox']})
        while True:
            result, url = await taobao(username, password, url, page)
            if 'passport' not in url:
                break
        if result:
            cookies = result
            return cookies
        else:
            return None
    except Exception as e:
        print(e)
        # logger.exception(e)


async def taobao(username, password, url, page):
    """
    淘宝登录主程序
    :param username: 用户名
    :param password: 密码
    :param url: 登录网址
    :return: 登录cookies
    """
    await page.goto(url)
    print('page.go' + url)
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    print('js加载完毕')
    # time.sleep(2000)
    # 从二维码页面点击到账号密码页面
    await page.evaluate('''document.getElementsByClassName('login-tab login-tab-r')[0].click()''')
    time.sleep(2)
    # 输入用户名，密码
    # time.sleep(2000)
    await page.evaluate('''document.getElementById("loginname").value=""''')
    await page.type('#loginname', username, {'delay': input_time_random()})  # delay是限制输入的时间
    await page.type('#nloginpwd', password, {'delay': input_time_random()})
    await page.evaluate('''document.getElementById("loginsubmit").click()''')
    await page.waitFor(2000)
    while True:
        if 'login' in page.url:
            while True:
                time.sleep(1)
                await download_pic(page)
                if await get_gap() <= 45:
                    await page.evaluate('''document.getElementsByClassName('JDJRV-img-refresh')[0].click()''')
                    pass
                else:
                    break
            elemnt = await page.J('.JDJRV-slide-btn')
            i = await elemnt.boundingBox()
            # 因为下载的图片是360大小所以要根据网页图片大小调整路径长度
            offsets, tracks = await get_tracks(await get_gap() * 278 / 360, 3, 'ease_out_expo')
            # 因为hover滑块之后鼠标在滑块中间,这个时候down之后,鼠标在坏块27像素之前移动都无法造成滑块移动
            lenth = i['x'] + 27
            high = i['y']
            await page.hover('.JDJRV-slide-btn')
            await page.mouse.down()
            await page.mouse.move(lenth, high)
            for x in tracks:
                # 正向
                # await page.hover('.JDJRV-slide-btn')
                lenth = lenth + x
                # await page.hover('.JDJRV-smallimg')
                await page.mouse.move(lenth, high)
            time.sleep(0.5)
            await page.mouse.up()
            await page.waitFor(2000)
            print(page.url)
        else:
            break
    cookies_list = await page.cookies()
    cookies = {}
    for cookie in cookies_list:
        cookies[cookie['name']] = cookie['value']
    new_cookie = ''
    for i in cookies:
        new_cookie += i + '=' + cookies[i] + ';'
    print('cookie页面的url' + page.url)
    return new_cookie, page.url


async def download_pic(page):
    """
    下载验证码图片
    :param page: 网页
    :return:
    """
    time.sleep(1)
    page_html = await page.content()
    pic_bs64 = re.search(r'<img src="data:image/png;base64,(.*?)"', page_html).groups()[0]
    imagedata = base64.b64decode(pic_bs64)
    with open('code.png', 'wb') as f:
        f.write(imagedata)
        print("识别图片")


async def get_gap():
    '''
    获取缺口偏移量
    img1: 不带缺口图片 Image.open(BytesIO(图片的2进制))
    img2: 带缺口图 Image.open(BytesIO())
    :return 缺口位置
    '''
    left = 39
    with open('jd_code.png', 'rb') as f:
        img1 = Image.open(BytesIO(f.read()))
    with open('code.png', 'rb') as f:
        img2 = Image.open(BytesIO(f.read()))
    for i in range(left, img1.size[0]):
        for j in range(img1.size[1]):
            if not await is_pixel_equal(img1, img2, i, j):
                left = i
                return left
    return left


async def is_pixel_equal(img1, img2, x, y):
    '''
    判断两个像素是否相同
    :param img1: 不带缺口图片
    :param img2: 带缺口图
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    '''
    # 取两个图片的像素点
    pix1 = img1.load()[x, y]
    pix2 = img2.load()[x, y]
    threshold = 60
    if (abs(pix1[0] - pix2[0]) < threshold and abs(pix1[1] - pix2[1]) < threshold and abs(
            pix1[2] - pix2[2]) < threshold):
        return True
    else:
        return False


# async def save_cookie(item):
#     collection.insert_one(item)
#
# async def del_cookie():
#     collection.delete_many({})


def input_time_random():
    return random.randint(100, 151)


async def run(username, password):
    # await del_cookie()
    (browser, page) = await creat_browser()
    url = 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F'
    cookie = await login(page, username, password, url)
    await close_browser(browser)
    return cookie


def main(username, password):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(run(username, password))
    loop.run_until_complete(task)
    return task.result()


if __name__ == '__main__':
    pass
