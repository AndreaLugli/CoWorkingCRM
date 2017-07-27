# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from locations.models import Location
from .models import Feed, Member
from plans.models import Subscription

APP_LOGIN_URL = reverse_lazy('app_login')
APP_INDEX_URL = reverse_lazy('app_index')

class app_login(View):
	def dispatch(self, *args, **kwargs):
		return super(app_login, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		template_name = "app_login.html"
		return render(request, template_name)

	def post(self, request, *args, **kwargs):
		email = request.POST['email']
		password = request.POST['password']

		user = authenticate(username = email, password = password)

		if user is not None:
			login(request, user)

			return HttpResponseRedirect(APP_INDEX_URL)
		else:
			return HttpResponseRedirect(APP_LOGIN_URL)		

class app_index(View):
	@method_decorator(login_required(login_url=APP_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(app_index, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		user = request.user
		if user.is_superuser or user.is_staff:
			return HttpResponseRedirect(APP_LOGIN_URL)

		email = user.email
		member_obj = Member.objects.get(email = email)
		account = member_obj.account_set.get()
		subscription_active_exists = Subscription.objects.filter(account = account, status = "ACT").exists()

		subs = Subscription.objects.filter(account = account, status = "ACT")

		locations_sub = []

		for sub in subs:
			locations_sub.append(sub.plan.location)
		feeds = Feed.objects.filter(location__in = locations_sub).order_by("-created_at")


		args = {
			"feeds" : feeds
		}

		template_name = "app_index.html"
		return render(request, template_name, args)

class app_bacheca_new(View):
	@method_decorator(login_required(login_url=APP_LOGIN_URL))
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(app_bacheca_new, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		user = request.user
		email = user.email
		member_obj = Member.objects.get(email = email)
		account = member_obj.account_set.get()
		subscription_active_exists = Subscription.objects.filter(account = account, status = "ACT").exists()

		subs = Subscription.objects.filter(account = account, status = "ACT")

		locations_sub = []

		for sub in subs:
			locations_sub.append(sub.plan.location)

		args = {
			"locations_sub" : locations_sub
		}

		template_name = "app_bacheca_new.html"
		return render(request, template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.user

		content = request.POST['content']
		location_id = request.POST['location']
		location = Location.objects.get(pk = location_id)

		Feed.objects.create(user = user, location = location, content = content)

		messages.success(request, 'Messaggio inviato con successo')

		url = reverse('app_bacheca_new')
		return HttpResponseRedirect(url)
