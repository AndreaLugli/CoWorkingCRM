# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Location(models.Model):
	name = models.CharField(max_length = 200)
	address = models.CharField(max_length = 200)

	hot_desks_total = models.IntegerField(default = 0)
	fix_desks_total = models.IntegerField(default = 0)

	class Meta:
		verbose_name = "Location"
		verbose_name_plural = "Locations"

	def __unicode__(self):
		return self.name			

class MeetingRoom(models.Model):
	name = models.CharField(max_length = 200)
	location = models.ForeignKey(Location)	
	seats = models.IntegerField()
	price = models.CharField(max_length = 200, blank = True, null = True)

	class Meta:
		verbose_name = 'Meeting room'
		verbose_name_plural = "Meeting rooms"

	def __unicode__(self):
		return self.name + " - " + self.location.name

class Office(models.Model):
	name = models.CharField(max_length = 200)
	location = models.ForeignKey(Location)	
	seats = models.IntegerField()

	class Meta:
		verbose_name = 'Office'
		verbose_name_plural = "Office"

	def __unicode__(self):
		return self.name + " - " + self.location.name