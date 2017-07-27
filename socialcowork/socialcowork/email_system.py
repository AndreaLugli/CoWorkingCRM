# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
#from socialcowork.tasks import send_mail_task
from django.conf import settings
from main.models import Member, ResetPassword
from datetime import datetime
import hashlib

IS_LOCAL = settings.IS_LOCAL

#def send_email(sender, to, content, subject):
	#if IS_LOCAL:
	#	send_mail_task(sender, to, content, subject)
	#else:
	#	send_mail_task.delay(sender, to, content, subject)	

def send_email_new_om(to, first_name, token):
	#sender = "team@edgecowork.com"
	#subject = "Welcome to the family"

	url = reverse('crm_om_setpassword', kwargs = {'token': token})

	#if IS_LOCAL:
	#	url = "http://127.0.0.1:8000" + url
	#else:
		#url = "http://app.edgecowork.com" + url

	url = "http://127.0.0.1:8000" + url

	print url

	content = "\
		Ciao %s,<br/>\
		Benvenuto a SocialCowork. Devi confermare l'account per poter amministrare una sede.<br/><br/>\
		Clicca <a href='%s'>qui</a> per creare una password<br>\
		Saluti!" % (first_name, url)

	#send_email(sender, to, content, subject)

def send_password_new_user(to, first_name, password):
	print password