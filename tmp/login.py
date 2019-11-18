# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/11/13 17:11
 @Auth : 明明
 @IDE  : PyCharm
 """

import asyncio
import sys

from pyppeteer import launch

sys.path.append(sys.path[0])
from setting import headless


async def main(base_url):
    browser = await launch(headless=headless, devtools=True, userDataDir='./userdata', args=['--disable-infobars'])
    page = await browser.newPage()
    width, height = 1366, 768
    await page.setViewport({'width': width, 'height': height})

    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    print('js加载完毕')
    await asyncio.sleep(2)

    await asyncio.sleep(2)
    await page.goto(base_url)

    cookies_list = await page.cookies()
    cookies = {}
    for cookie in cookies_list:
        cookies[cookie['name']] = cookie['value']
    await browser.close()
    return cookies


def run(url):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(main(url))
    loop.run_until_complete(task)
    cookie = task.result()
    print(cookie)
    return cookie


if __name__ == '__main__':
    url = "https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E5%B0%8F%E7%B1%B3&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=3894&sst0=1573633538854&lkt=1%2C1573633538752%2C1573633538752"
    url = "https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E5%B0%8F%E7%B1%B3&ie=utf8&_sug_=n&_sug_type_="
    run(url)
