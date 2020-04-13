#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import smtplib
from email.header import Header
from email.mime.text import MIMEText

email_host = "smtp.exmail.qq.com"
email_port = 465
email_from = "monitor-system@skieer.com"
email_password = ""  # TODO 填入授权码
email_to = ["wangrongming@skieer.com"]


def send(title, content, content_type="html"):
    message = MIMEText(content, content_type, 'utf-8')
    message['Subject'] = Header(title, 'utf-8')
    message['From'] = email_from
    message['To'] = ";".join(email_to)

    smtp_obj = smtplib.SMTP_SSL(host=email_host, port=email_port)
    smtp_obj.login(email_from, email_password)
    smtp_obj.sendmail(email_from, email_to, message.as_string())


if __name__ == '__main__':
    title_info = "客服会话数据采集异常"
    content_info = ""
    send(title_info, content_info)
