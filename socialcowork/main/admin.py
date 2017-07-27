# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Feed

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
	list_display = ['user', 'created_at']

