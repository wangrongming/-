import logging

import requests
import tenacity
from tenacity import stop_after_attempt, wait_fixed, stop_after_delay

time = 0


def test(retry_state):
    print("在test之后 {}".format(retry_state))

# stop=stop_after_attempt(3) 让它重试3次后不再重试并抛出异常
# @after 添加终止条件
# wait=wait_fixed(0.1) 每隔0.1s 请求一次
# wait=wait_random(min=1, max=2) 每隔随机时间 请求一次
# wait=wait_exponential(multiplier=2, min=3, max=100) 2^n * multiplier, n为重试次数，但最多间隔10s
# retry=retry_if_exception_type(IOError)  带有出发条件
# stop=stop_after_delay(1) 5s之后不再重试
# after=test 每次在执行test()函数之后再执行重试方法
@tenacity.retry(stop=stop_after_delay(1), wait=wait_fixed(0.1), after=test)
def get_info():
    url = 'https://www.baidu.com/'
    # url = 'https://www.google.com/'
    global time
    time += 1
    print(time)
    response = requests.get(url=url)
    if response.status_code != 200:
        return response.text
    raise Exception


if __name__ == '__main__':
    test(time)
    get_info()
