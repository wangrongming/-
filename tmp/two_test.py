import json
import re
import time
import traceback
from hashlib import sha1
from urllib.parse import urljoin

import execjs
import requests
import tenacity
from lxml import etree
from readability import Document
from tenacity import stop_after_attempt, wait_fixed

cookies_new = {}
cookies_index = {}
proxies = {}


def get_proxy(retry_state):
    global proxies
    while True:
        url1 = 'http://proxy.yuntingai.com/proxy/getProxy/14'
        try:
            res = requests.get(url1, timeout=3)
            if res.status_code != 200:
                continue
            proxy_info = res.json()
            if proxy_info.get('trueIp'):
                if proxy_info['type'] == 'http':
                    proxy_info['type'] = 'http'
                else:
                    proxy_info['type'] = 'socks5'
                type_info = proxy_info['type']
                name = proxy_info['name']
                password = proxy_info['password']
                host = proxy_info['host']
                port = proxy_info['port']
                proxies = {
                    'https': "{}://{}:{}@{}:{}".format(type_info, name, password, host, port),
                    'http': "{}://{}:{}@{}:{}".format(type_info, name, password, host, port),
                }
                break
            else:
                time.sleep(2)
                continue
        except Exception:
            print(traceback.format_exc())
            time.sleep(3)


class GZH(object):
    """
    公众号采集
    """

    def __init__(self, key_word):
        self.base_url = "https://weixin.sogou.com/weixin?"
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 " \
                          "(KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
        self.key_word = key_word
        self.cookies = None
        self.index_url = None
        self.uigs_para = None

        self.url_pattern = re.compile(r'<h3>.*?<a.*?href=\"(.*?)\".*?<\/h3>', re.S)
        self.uuid_pattern = re.compile(r'uuid.*?"(.*?)";', re.S)
        self.amp_pattern = re.compile(r'amp;')
        self.title_pattern = re.compile(r'var msg_title.*?"(.*?)"')
        self.nickname_pattern = re.compile(r'var nickname.*?"(.*?)"')
        self.article_desc_pattern = re.compile(r'var msg_desc.*?"(.*?)"')
        self.publish_time_pattern = re.compile(r',s=.*?"(.*?)"')
        self.source_url_pattern = re.compile(r'var msg_source_url = \'(.*?)\'')
        self.content_pattern = re.compile(r'<[^>]*>')
        self.msg_id_pattern = re.compile(r'var appmsgid.*?(\d+).*?;')
        self.kw_pattern = re.compile(r'query=(.*?)&')
        self.migrate_pattern = re.compile(r'var transfer_target_link.*?\'(.*?)\';')
        self.type_pattern = re.compile(r'&type=(\d+)')
        self.mv_title_pattern = re.compile(r'd.title.*?"(.*?)";')
        self.mv_nk_pattern = re.compile(r'd.nick_name.*?"(.*?)";')
        self.mv_ct_pattern = re.compile(r'd.ct.*?"(.*?)";')
        self.mv_mid_pattern = re.compile(r'd.mid.*?"(\d+)";')
        self.gzh_url_pattern = re.compile(r'<a.*?href="(.*?)"><em><!--red_beg-->.*?<!--red_end--></em></a>')
        self.json_pattern = re.compile(r'var msgList.*?{"list":(.*?)};')

    @tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1), after=get_proxy)
    def index(self, page):
        params = {
            'oq': '',
            'query': self.key_word,
            '_sug_type_': '1',
            'sut': '0',
            'lkt': '0,0,0',
            's_from': 'input',
            'ri': '0',
            '_sug_': 'n',
            'type': '2',
            'sst0': int(time.time()),
            'page': str(page),
            'ie': 'utf8',
            'p': '40040108',
            'dp': '1',
            'w': '01015002',
            'dr': '1',
        }
        headers = {
            'Host': 'weixin.sogou.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://weixin.sogou.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        response = requests.get(url=self.base_url, params=params, headers=headers, proxies=proxies)
        html = response.text
        cookies = {}
        for cookie in response.cookies.items():
            cookies[cookie[0]] = cookie[1]
        url_pattern = re.compile(r'<h3>.*?<a.*?href=\"(.*?)\".*?<\/h3>', re.S)
        uigs_para = re.findall(r'var.*?uigs_para.*?=.*?({.*?});', html, re.S)
        uigs_para = re.sub(r'\s|\n|\t', "", uigs_para[0])
        uigs_para = json.loads(re.sub(r'passportUserId.*?\?.*?0"', "0", uigs_para))
        url_li = url_pattern.findall(html)
        self.cookies = cookies
        self.index_url = response.url
        self.uigs_para = uigs_para
        for url in url_li:
            item = {
                "url": url,
            }
            yield item

    @tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1), after=get_proxy)
    def index_cookie(self, page):
        params = {
            'oq': '',
            'query': self.key_word,
            '_sug_type_': '1',
            'sut': '0',
            'lkt': '0,0,0',
            's_from': 'input',
            'ri': '0',
            '_sug_': 'n',
            'type': '2',
            'sst0': int(time.time()),
            'page': str(page),
            'ie': 'utf8',
            'p': '40040108',
            'dp': '1',
            'w': '01015002',
            'dr': '1',
        }
        headers = {
            'Host': 'weixin.sogou.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://weixin.sogou.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        response = requests.get(url=self.base_url, params=params, headers=headers, proxies=proxies)
        cookies = {}
        for cookie in response.cookies.items():
            cookies[cookie[0]] = cookie[1]
        self.cookies = cookies

    @tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1))
    def detail_one(self, item):
        try:
            global cookies_new
            cookies = self.cookies
            url = item['url']
            url = urljoin("https://weixin.sogou.com/link?", url)
            url = self.url_js_index(url)
            cookie = ""
            for value in cookies:
                cookie += "{}={};".format(value, cookies[value])
            for value in cookies_new:
                cookie += "{}={};".format(value, cookies_new[value])

            headers = {
                'Host': 'weixin.sogou.com',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': self.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': self.index_url,
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cookie': cookie
            }
            response = requests.request("GET", url, headers=headers, proxies=proxies)
            html = response.content.decode("utf-8")
            if "seccodeInput" in html:
                get_proxy(1)
                self.index_cookie(1)
                self.generate_cookie()
                raise Exception
            url_str = re.findall(r"<script>(.*?)url\.replace", html, re.S)
            command = """
            function url (){
                %s
                return url;
            };
            """ % url_str[0]
            ctx = execjs.compile(command)
            final_url = ctx.call("url")
            return response.url, final_url
        except Exception:
            print(traceback.format_exc())
            raise Exception

    @tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1), after=get_proxy)
    def article(self, referer_url, url):
        html = None
        try:
            headers = {
                'Host': 'mp.weixin.qq.com',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': self.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': referer_url,
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
            html = requests.get(url, headers=headers, proxies=proxies).text
            title = etree.HTML(html).xpath("//*[@id='activity-name']/text()")
            if not title:
                title = etree.HTML(html).xpath("//*[@id='video_title']/text()")
            print("文章标题", re.sub(r"\s|\n|\t", "", title[0]))
            # print("文章内容", response.text)
        except Exception:
            print(traceback.format_exc())
            print(html)
            raise Exception

    def main(self):
        try:
            get_proxy(1)
            for page in range(1, 11):
                print("当前开始采集 第{}页内容".format(page))
                for item in self.index(page):
                    if not cookies_new:
                        self.generate_cookie()
                    if cookies_new:
                        referer_url, url = self.detail_one(item)
                        self.article(referer_url, url)
                    else:
                        print("第{} 页 构建cookie失败 跳过当前页".format(page))
                        break
        except Exception:
            print(traceback.format_exc())

    @tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1), after=get_proxy)
    def parse_detail(self, share_url, response):
        item = {}
        html = response.content.decode()
        url = share_url
        # print(url)
        if '<title>帐号已迁移</title>' in html:
            migrate_url = self.migrate_pattern.search(html).group(1)
            migrate_url = self.amp_pattern.sub('', migrate_url)
            migrate_res = requests.get(migrate_url,
                                       headers={'user-agent': self.user_agent},
                                       proxies=proxies, timeout=3)
            self.parse_detail(migrate_url, migrate_res)
        elif '该内容已被发布者删除' in html:
            return
        else:
            print("url:>" + url)
            if '<title>视频</title>' in html:
                title = self.mv_title_pattern.search(html).group(1)
                gzh_info = {}
                nickname = self.mv_nk_pattern.search(html).group(1)
                gzh_info['nickname'] = nickname
                gzh_info['gzh_desc'] = ''
                gzh_info['wx_num'] = ''
                article_desc = ''
                publish_time = self.mv_ct_pattern.search(html).group(1)
                st = time.localtime(int(publish_time))
                publish_time = time.strftime('%Y-%m-%d', st)
                msg_id = self.mv_mid_pattern.search(html).group(1)
                doc = Document(html).summary()
                content = self.content_pattern.sub('', doc).strip()
                article_source_url = ''
                item['gzh_info'] = gzh_info
                item['article_url'] = url
                item['title'] = title
                item['article_desc'] = article_desc
                item['publish_time'] = publish_time
                item['page_source'] = doc
                item['content'] = content
                item['article_source_url'] = article_source_url
                item['msg_id'] = msg_id
                item['kw'] = self.key_word
                item['kw_source'] = self.key_word  # TODO kw_source
                item['insert_at'] = int(time.time() * 1000)
                s = sha1()
                s.update((title + msg_id + self.key_word + nickname).encode())
                item['article_fingerprint'] = s.hexdigest()
                # if self.db.get_collection(PINGAN_COLLECTION).find_one(
                #         {'article_fingerprint': item['article_fingerprint']}):
                #     pass
                # else:
                #     self.db.get_collection(PINGAN_COLLECTION).insert_one(item)
                print(item)
            else:
                try:
                    try:
                        title = self.title_pattern.search(html).group(1)
                    except Exception as e:
                        # self.logger.exception(str(e) + '\n---->' + url)
                        title = ''
                    gzh_info = {}
                    try:
                        nickname = self.nickname_pattern.search(html).group(1)
                    except Exception as e:
                        # self.logger.exception(str(e) + '\n---->' + url)
                        nickname = ''
                    info = etree.HTML(html).xpath('//span[@class="profile_meta_value"]/text()')
                    if info:
                        try:
                            gzh_desc = info[1].strip()
                            wx_num = info[0].strip()
                        except:
                            gzh_desc = info[0].strip()
                            wx_num = ''
                    else:
                        gzh_desc = ''
                        wx_num = ''
                    gzh_info['nickname'] = nickname
                    gzh_info['gzh_desc'] = gzh_desc
                    gzh_info['wx_num'] = wx_num
                    article_desc = self.article_desc_pattern.search(html).group(1)
                    publish_time = self.publish_time_pattern.search(html).group(1)
                    msg_id = self.msg_id_pattern.search(html).group(1)
                    doc = Document(html).summary()
                    content = self.content_pattern.sub('', doc).strip()
                    article_source_url = self.source_url_pattern.search(html).group(1)
                    item['gzh_info'] = gzh_info
                    item['article_url'] = url
                    item['title'] = title
                    item['article_desc'] = article_desc
                    item['publish_time'] = publish_time
                    item['page_source'] = doc
                    item['content'] = content
                    item['article_source_url'] = article_source_url
                    item['msg_id'] = msg_id
                    item['kw'] = self.key_word
                    item['kw_source'] = self.key_word
                    item['insert_at'] = int(time.time() * 1000)
                    s = sha1()
                    s.update((title + msg_id + self.key_word + nickname).encode())
                    item['article_fingerprint'] = s.hexdigest()
                    print(item)
                    # if self.db.get_collection(PINGAN_COLLECTION).find_one(
                    #         {'article_fingerprint': item['article_fingerprint']}):
                    #     pass
                    # else:
                    #     self.db.get_collection(PINGAN_COLLECTION).insert_one(item)
                    #     print(item)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    pass
                    # self.logger.exception(str(e) + '\n---->' + url)

    @tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1), after=get_proxy)
    def generate_cookie(self):
        global cookies_new
        cookies = self.cookies
        su_id = cookies['SUID']
        ip_loc = cookies['IPLOC']
        snu_id = cookies['SNUID']
        ab_test = cookies['ABTEST']

        cookies_new = {}
        # 1 SNUID IPLOC => ABTEST SUID
        headers = {
            'Host': 'www.sogou.com',
            'Connection': 'keep-alive',
            'User-Agent': self.user_agent,
            'Accept': 'text/css,*/*;q=0.1',
            'Referer': self.index_url,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'SNUID={}; IPLOC={}'.format(snu_id, ip_loc),
        }
        url = "https://www.sogou.com/sug/css/m3.min.v.7.css"
        response = requests.get(url=url, headers=headers, proxies=proxies)
        for cookie in response.cookies.items():
            if cookie[0] in ['SUID']:
                cookies_new[cookie[0]] = cookie[1]

        # 2 ABTEST SNUID IPLOC SUID SUID=> JSESSIONID
        headers = {
            'Host': 'weixin.sogou.com',
            'Connection': 'keep-alive',
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Referer': self.index_url,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'ABTEST={};SNUID={};IPLOC={};SUID={};SUID={};'.format(ab_test, snu_id, ip_loc, su_id,
                                                                            cookies_new['SUID']),
        }
        url = "https://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp"
        response = requests.get(url=url, headers=headers, proxies=proxies)
        for cookie in response.cookies.items():
            if cookie[0] in ['JSESSIONID']:
                cookies_new[cookie[0]] = cookie[1]

        # 3 SNUID IPLOC SUID => ABTEST SUID
        headers = {
            'Host': 'pb.sogou.com',
            'Connection': 'keep-alive',
            'User-Agent': self.user_agent,
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': self.index_url,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'SNUID={};IPLOC={};SUID={};'.format(snu_id, ip_loc, cookies_new['SUID']),
        }
        url = "https://pb.sogou.com/pv.gif?https://pb.sogou.com/pv.gif?"
        params = self.uigs_para
        params['uigs_refer'] = 'https://weixin.sogou.com/'
        params['exp_id'] = 'null_0-null_1-null_2-null_3-null_4-null_5-null_6-null_7-null_8-null_9'
        response = requests.get(url=url, headers=headers, params=params, proxies=proxies)
        for cookie in response.cookies.items():
            if cookie[0] in ['SUV']:
                cookies_new[cookie[0]] = cookie[1]
        print("cookie_new:", cookies_new)

    @staticmethod
    def url_js_index(href):
        command = """
        function gen_url(href) {
        var b = Math.floor(100 * Math.random()) + 1,
        a = href.indexOf("url="),
        c = href.indexOf("&k="); 
        - 1 !== a && -1 === c && (a = href.substr(a + 4 + parseInt("21") + b, 1), href += "&k=" + b + "&h=" + a)
        return href
    };"""
        ctx = execjs.compile(command)
        return ctx.call("gen_url", href)


if __name__ == '__main__':
    key_word_li = ["小米"]
    for word in key_word_li:
        gzh = GZH(key_word=word)
        gzh.main()
