# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Location, MeetingRoom, Office

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display = ['name', 'hot_desks_total', 'fix_desks_total']

@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
	pass

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
	pass
