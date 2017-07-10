#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText


class SenderMail(object):
    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = "smtp.163.com"  # 设置服务器
        self.mail_user = "wswenyue@163.com"  # 用户名
        self.mail_pass = "邮箱登录密码"  # 口令
        #
        self.sender = 'wswenyue@163.com'
        self.receivers = ['wswenyue@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    def send(self, msg):
        message = MIMEText(msg, 'html', 'utf-8')
        message['From'] = self.sender
        message['Subject'] = Header("Email Subject", 'utf8').encode()
        message['To'] = '<' + self.receivers[0] + '>'
        try:
            smtp = smtplib.SMTP(self.mail_host, 25)
            smtp.login(self.mail_user, self.mail_pass)
            smtp.sendmail(self.sender, self.receivers, message.as_string())
            print unicode("邮件发送成功", "utf8")
        except Exception, e:
            print e.args
            print unicode("Error: 无法发送邮件", "utf8")

# SenderMail().send("hello")
