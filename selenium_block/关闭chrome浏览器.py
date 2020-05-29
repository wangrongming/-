from selenium import webdriver
from selenium.webdriver.chrome.service import Service

"""
ChromeDriver是轻量级的服务，在单任务或不需要频繁启动浏览器的情况下，
使用driver.quit()关闭浏览器，可以正常结束ChromeDriver进程。
若在一个比较大的 测试套件中频繁的启动关闭，
会增加一个比较明显的延时导致浏览器进程不被关闭的情况发生，
为了避免这一状况我们可以通过 ChromeDriverService 来控制ChromeDriver进程的生死，
达到用完就关闭的效果避免进程占用情况出现（Running the  server in a child process）
"""

# chromedriver.exe的位置写在Service的XXX部分
c_service = Service('xxx')
c_service.command_line_args()
c_service.start()
driver = webdriver.Chrome()
driver.get("http://www.baidu.com")

driver.quit()
c_service.stop()
