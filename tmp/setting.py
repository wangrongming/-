# encoding: utf-8
"""
@author: Liu
@file: setting.py.py
@time: 2019/3/28 2:48 PM
"""
import os
import platform

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOT_NAME = 'sw_gzh'

SPIDER_MODULES = ['sw_gzh.spiders']
NEWSPIDER_MODULE = 'sw_gzh.spiders'

USER_AGENT = 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)'

ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 24

COOKIE = 'CXID=B43F2592105F8C3A10376EABCB44ED01; SUID=7D498D3D5B68860A5BB4E5E9000B5231; SUV=002270163D8D40A75BC6874F37CAF788; IPLOC=CN4403; weixinIndexVisited=1; ABTEST=0|1552616111|v1; JSESSIONID=aaaaQNsvvCTrs658G1RLw; PHPSESSID=gmn2ki18h71iekv1tls4gkv6p0; sct=7; SNUID=44471E7105008321A5D560B40601A27C'
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

DOWNLOAD_TIMEOUT = 10

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'sw_gzh.middlewares.SwGzhSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'sw_gzh.middlewares.CookieSwitchDownloaderMiddleware': 300,
    'sw_gzh.middlewares.ProxyUserAgentDownloaderMiddleware': 200,
    'sw_gzh.middlewares.SourceDownloaderMiddleware': 100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'sw_gzh.extensions.IniLogstash': 233,
}

LOGSTASH_ENABLED = True
LOGSTASH_HOST = 'localhost'
LOGSTASH_PORT = 5959

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'sw_gzh.pipelines.SwGzhPipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline': 900
}

LOG_LEVEL = 'DEBUG'  # log日志级别
LOG_FILE = os.path.join(base_dir, 'sw_gzh/log/spider.log')
LOG_STDOUT = True

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
]

# Redis配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PARAMS = {}
REDIS_KEY = 'gzhspiderspider:start_urls'
FINGERPRINT_SET_KEY = 'item_fingerprint'
CEM_SET_KEY = 'weixin_cem_kw'
PINGAN_SET_KEY = 'weixin_pingan_kw'
GZH_SET_KEY = 'weixin_gzh_kw'

# MongoDB配置
DB = 'wechat'
PINGAN_COLLECTION = 'PingAnTech'
CEM_COLLECTION = 'CEM'
COOKIES_COLLECTION = 'weixin_cookie'
KW_COLLECTION = 'weixin_article_searchkey'
SOURCE_COLLECTION = 'weixin_article_source'
GZH_COLLECTION = 'gzh_search'
GZH_KW_COLLECTION = 'weixin_gzh'
USERNAME = 'vjbdhmpv'
PASSWORD = 'yClTEYwC9mUQ'
MONGO_HOST = '10.1.1.127'
MONGO_PORT = '27017'
MONGO_URI = "mongodb://{}:{}@{}:{}/{}?".format(USERNAME, PASSWORD, MONGO_HOST, MONGO_PORT, DB)
# MONGO_URI = "mongodb://192.168.0.238:21018"

# scrapy_redis
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

SCHEDULER = "scrapy_redis.scheduler.Scheduler"

SCHEDULER_PERSIST = True

BASE_URL = 'https://weixin.sogou.com/weixin?query={}&_sug_type_=&sut=635&lkt=0%2C0%2C0&s_from=input&_sug_=y&type=2&page={}&ie=utf8'

ONE_DAY_URL = 'https://weixin.sogou.com/weixin?usip=&query={}&ft=&tsn=1&et=&interation=&type=2&wxid=&page={}&ie=utf8'

GZH_BASE_URL = 'https://weixin.sogou.com/weixin?query={}&type=1&s_from=input&ie=utf8&_sug_=n&_sug_type_='

# proxy配置
PROXY_PORT = 31281
PROXY_PROTOCOL = 'http'
PROXY_USERNAME = 'hty001'
PROXY_PASSWORD = 'Hty8899'
PROXY_URL = 'http://123.206.231.183:8080/proxy/getProxy/{}'
TASK_ID = 254

if 'Win' in platform.system():
    headless = False
else:
    headless = True
