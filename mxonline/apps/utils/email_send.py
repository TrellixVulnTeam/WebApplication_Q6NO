# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/8/16 18:22'

import random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from mxonline.settings import EMAIL_FROM


def send_register_email(email, send_type="register"):
	email_record = EmailVerifyRecord()
	code = random_str(16)
	email_record.code = code
	email_record.email = email
	email_record.send_type = send_type
	email_record.save()         # 保存到数据库
	# 发送邮件
	email_title = ""
	email_body = ""
	if send_type == "register":
		email_title = "慕学在线网注册激活链接"
		email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)
		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])     # 发送状态，email必须为列表
		if send_status:
			pass
	elif send_type == "forget":
		email_title = "慕学在线网重置链接"
		email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/reset/{0}".format(code)
		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])     # 发送状态，email必须为列表
		if send_status:
			pass

def random_str(randomlength=8):
	str = ''
	chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcefghijklmnopqrstuvwxyz0123456789"
	length = len(chars) - 1
	for i in range(randomlength):
		str += chars[random.randint(0, length)]
	return str