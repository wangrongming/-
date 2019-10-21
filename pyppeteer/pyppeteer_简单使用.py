import asyncio
from pyppeteer import launch


async def main():
    browser = await launch(headless=False, devtools=True, userDataDir='./userdata', args=['--disable-infobars'])
    page = await browser.newPage()
    width, height = 1366, 768
    await page.setViewport({'width': width, 'height': height})
    await page.goto('http://quotes.toscrape.com/js/')
    await page.screenshot(path='example.png')
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
