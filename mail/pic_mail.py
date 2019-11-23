# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @Time : 2019/11/20 16:53
 @Auth : 明明
 @IDE  : PyCharm
 """
import logging
import smtplib
import sys
import traceback
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger(__name__)


def pic_content():
    import requests

    url = "http://mp.weixin.qq.com/rr"

    querystring = {"timestamp": "1574241431", "src": "3", "ver": "1",
                   "signature": "rFf0mlUPPUaUNPpJpIu5Yrk7Btf2c9vwq7xm7v7zDVhlKOFmGmpTyr52wAEY2Q3UNj7spHGzdeT8GDo4pLJYNVrT2Rfery4LVYZcnn0jHEE="}

    headers = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cookie': "pgv_pvi=1434090496; pgv_pvid=3882778600; rewardsn=; wxtokenkey=777",
        'cache-control': "no-cache",
        'Postman-Token': "b78a1458-6c30-4681-af32-f2ab1494229f"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    content = response.content
    return content


def send_mail(subject, pic=None):
    msg_from = 'monitor-system@skieer.com'  # 发送方邮箱
    passwd = 'Harry1234'  # 填入发送方邮箱的授权码

    msg_to_list = ['wangrongming@skieer.com']  # 收件人邮箱
    msg_to = ";".join(msg_to_list)
    content = MIMEText('<html><h3>请用手机微信扫描下方二维码</h3><body><img src="cid:imageid" alt="imageid"></body></html>', 'html',
                       'utf-8')
    msg = MIMEMultipart('related')
    msg.attach(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to

    img = MIMEImage(pic)
    img.add_header('Content-ID', 'imageid')
    msg.attach(img)

    try:
        s = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        logger.info("邮件 发送成功")

    except Exception as e:
        logger.info("邮件 发送失败 {}".format(traceback.format_exc()))


if __name__ == '__main__':
    subject = "搜狗搜索——微信登陆"
    # content = pic_content()
    # print(content)
    file = open("1.png", "rb")
    img_data = file.read()
    file.close()
    send_mail(subject, img_data)
