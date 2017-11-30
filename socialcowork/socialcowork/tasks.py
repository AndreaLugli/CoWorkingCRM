# -*- coding: utf-8 -*-
from django.core.mail import send_mail

def send_mail_task(sender, to, content, subject):
	send_mail(subject, content, sender, [to], fail_silently = False, html_message = content)