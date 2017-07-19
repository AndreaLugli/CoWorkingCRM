# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Member(User):
	cellphone = models.CharField(max_length = 200, null = True, blank = True)
	job_title = models.CharField(max_length = 200, null = True, blank = True)
	profile_picture = models.CharField(max_length = 200, null = True, blank = True)
	is_primary_user = models.BooleanField(default = False)

class Account(models.Model):
	logo = models.CharField(max_length = 200, null = True, blank = True)
	name = models.CharField(max_length = 200)

	created_at = models.DateTimeField(auto_now_add = True)
	is_freelancer = models.BooleanField(default = False)
	members = models.ManyToManyField(Member)
	
	STATUS = (
		('ACT', "Activo"),
		('INA', 'Inactivo'),
	)

	status = models.CharField(max_length = 3, choices = STATUS, default = "ACT")

	class Meta:
		verbose_name = "Account"
		verbose_name_plural = "Accounts"

	def __unicode__(self):
		return self.name		

class ResetPassword(models.Model):
	user = models.ForeignKey(Member)
	token = models.CharField(max_length = 300)
	used = models.BooleanField(default = False)

	class Meta:
		verbose_name = "Reset Password"
		verbose_name_plural = "Reset Password"

	def __unicode__(self):
		return self.user.get_full_name()