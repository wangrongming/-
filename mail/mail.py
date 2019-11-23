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
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger(__name__)


def send_mail(subject, content):
    msg_from = '1768389896@qq.com'  # 发送方邮箱
    # passwd = 'tihqwaydawovbeac'  # 填入发送方邮箱的授权码
    passwd = 'oykdlefnnmcebabc'  # 填入发送方邮箱的授权码
    msg_to_list = ['wangrongming@skieer.com']  # 收件人邮箱
    msg_to = ";".join(msg_to_list)

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        logger.info("邮件 发送成功")

    except Exception as e:
        logger.info("邮件 发送失败 {}".format(e))


if __name__ == '__main__':
    subject = "搜索微信登陆"
    content = "请用手机微信扫描下方二维码"
    send_mail(subject, content)
