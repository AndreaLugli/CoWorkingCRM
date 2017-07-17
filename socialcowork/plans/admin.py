# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Plan, Subscription, Invoice

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
	list_display = ['name', 'location']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ['account', 'plan_location', 'plan_name',]

	def plan_name(self, obj):
		return obj.plan.name
	def plan_location(self, obj):
		return obj.plan.location.name

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	pass
