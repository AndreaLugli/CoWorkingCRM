# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from locations.models import Location, Office
from main.models import Account
import calendar

class Plan(models.Model):
	name = models.CharField(max_length = 200)
	location = models.ForeignKey(Location)
	price = models.IntegerField()
	meeting_room_hours = models.IntegerField(blank = True, null = True)
	is_active = models.BooleanField(default = True)
	office = models.ForeignKey(Office, blank = True, null = True)

	TYPES = (
		("HD", "Hot Desk"),
		("FD", "Fix Desk"),
		("PO", "Private Office")
	)

	type_of_plan = models.CharField(max_length = 3, choices = TYPES)
	
	class Meta:
		verbose_name = "Plan"
		verbose_name_plural = "Plans"

class Subscription(models.Model):
	account = models.ForeignKey(Account)
	plan = models.ForeignKey(Plan)

	STATUS_CODE = (
		("ACT", "Attivo"),
		("INA", "Inattivo"),
	)

	status = models.CharField(max_length = 3, choices = STATUS_CODE, default = "ACT")

	created_at = models.DateField(auto_now_add = True)
	#created_at.editable=True

	class Meta:
		verbose_name = "Subscription"
		verbose_name_plural = "Subscriptions"

class Invoice(models.Model):
	account = models.ForeignKey(Account)
	subscription = models.ManyToManyField(Subscription)
	extra_mr_to_pay = models.IntegerField(default = 0)
 	MONTHS_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]
	month = models.CharField(max_length=9, choices=MONTHS_CHOICES, default='1')
	year = models.IntegerField()
	date_paid = models.DateField(blank = True, null = True)
	is_paid = models.BooleanField(default = False)

	def get_planes(self):
		all_subs = self.subscription.all()
		list_planes = []
		for sub in all_subs:
			plan = sub.plan.get_type_of_plan_display()
			list_planes.append(plan)

		return ", ".join(list_planes)

	def get_period(self):
		month = self.month
		year = self.year

		return str(month) + "/" + str(year)

	def get_locations(self):
		all_subs = self.subscription.all()
		list_locations = []
		for sub in all_subs:
			location = sub.plan.location.name
			list_locations.append(location)

		return ", ".join(set(list_locations))

	def monthly_total(self):
		all_subs = self.subscription.all()
		total_to_pay_only_rent = 0
		for sub in all_subs:
			monthy_rent = sub.plan.price
			total_to_pay_only_rent = total_to_pay_only_rent + int(monthy_rent)

		return total_to_pay_only_rent


	def total_to_pay(self):
		monthly_total = self.monthly_total()

		return monthly_total + int(self.extra_mr_to_pay)

	class Meta:
		verbose_name='Invoice'
		verbose_name_plural='Invoices'




