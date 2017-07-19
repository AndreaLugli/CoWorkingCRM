# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from socialcowork.email_system import send_email_new_om
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render
from datetime import datetime, timedelta, date
from locations.models import Location, MeetingRoom, Office
from plans.models import Plan, Subscription, Invoice
from main.models import Account, Member, ResetPassword
import hashlib

CRM_LOGIN_URL = reverse_lazy("crm_login")
CRM_INDEX_URL = reverse_lazy("crm_index") 

class crm_login(View):
	def dispatch(self, *args, **kwargs):
		return super(crm_login, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		template_name = "crm_login.html"
		return render(request, template_name)

	def post(self, request, *args, **kwargs):
		email = request.POST['email']
		password = request.POST['password']

		user = authenticate(username = email, password = password)

		if user is not None:
			login(request, user)

			return HttpResponseRedirect(CRM_INDEX_URL)
		else:

			return HttpResponseRedirect(CRM_LOGIN_URL)

class crm_payment(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_payment, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		user = request.user
		is_staff = user.is_staff
		is_superuser = user.is_superuser

		today = datetime.today()
		current_month = today.month
		current_year = today.year

		current_invoices = get_invoices()

		not_paid_invoices = Invoice.objects.filter(is_paid = False)

		locations = Location.objects.all()

		invoice_paid = Invoice.objects.filter(is_paid = True)

		total_income = 0
		for invoice in invoice_paid:
			total_to_pay = invoice.total_to_pay()
			total_income = total_income + total_to_pay

		if is_staff and not is_superuser:
			locations = locations.filter(office_managers = user)
			current_invoices = current_invoices.filter(subscription__plan__location__office_managers = user)
			not_paid_invoices = not_paid_invoices.filter(subscription__plan__location__office_managers = user)
			invoice_paid = invoice_paid.filter(subscription__plan__location__office_managers = user)

		data = {
			"locations" : locations,
			"total_income" : total_income,
			"current_invoices" : current_invoices,
			"not_paid_invoices" : not_paid_invoices,
			"invoice_paid" : invoice_paid
		}

		template_name = "crm_payment.html"
		return render(request, template_name, data)


def get_invoices():
	today = datetime.today()
	current_month = today.month
	current_year = today.year

	first_day_this_month = datetime(current_year, current_month, 1)

	exists_invoice_this_month = Invoice.objects.filter(month = current_month, year = current_year).exists()	

	list_invoices = []

	if exists_invoice_this_month:
		list_invoices = Invoice.objects.filter(month = current_month, year = current_year)
	else:
		all_subscription = Subscription.objects.filter()

		all_active_subs = all_subscription.select_related('plan').filter(
			status = "ACT", 
			created_at__lt = first_day_this_month
		)

		for sub in all_active_subs:
			account = sub.account
			monthy_rent = sub.plan.price

			extra_mr_to_pay = 0

			#Last month extra booking

			invoice_obj, created = Invoice.objects.get_or_create(
				account = account,
				month = current_month, 
				year = current_year
			)

			invoice_obj.subscription.add(sub)

			old_extra_mr_to_pay = invoice_obj.extra_mr_to_pay
			new_extra_mr_to_pay = int(extra_mr_to_pay) + old_extra_mr_to_pay
			invoice_obj.extra_mr_to_pay = new_extra_mr_to_pay
			invoice_obj.save()

			list_invoices.append(invoice_obj)

	return list_invoices

class crm_locations(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_locations, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		user = request.user
		is_staff = user.is_staff
		is_superuser = user.is_superuser
	
		locations = Location.objects.all()

		if is_staff and not is_superuser:
			locations = locations.filter(office_managers = user)		

		for loc in locations:
			meeting_room = MeetingRoom.objects.filter(location = loc).count()
			loc.meeting_room = meeting_room

			office_total = Office.objects.filter(location = loc).count()
			loc.office_total = office_total

			subscriptions = Subscription.objects.filter(status = "ACT", plan__location = loc)

			hot_desk_active = subscriptions.filter(plan__type_of_plan = "HD").count()
			loc.hd_active = hot_desk_active

			fix_desks_active = subscriptions.filter(plan__type_of_plan = "FD").count()
			loc.fd_active = fix_desks_active

			private_offices_active = subscriptions.filter(plan__type_of_plan = "PO").count()
			loc.po_active = private_offices_active


		data = {
			"locations" : locations
		}

		template_name = "crm_locations.html"
		return render(request, template_name, data)

class crm_locations_new(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_new, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		template_name = "crm_locations_new.html"
		return render(request, template_name)

	def post(self, request, *args, **kwargs):

		nome = request.POST['nome']
		indirizzo = request.POST['indirizzo']
		hot_desk = request.POST['hot_desk']
		fix_desk = request.POST['fix_desk']

		new_location = Location.objects.create(
			name = nome,
			address = indirizzo,
			hot_desks_total = hot_desk,
			fix_desks_total = fix_desk
		)

		meeting_rooms = request.POST.get('meeting_rooms', 0)

		for meeting_rooms_id in range(1, int(meeting_rooms) + 1):

			meeting_room_label_name = 'meeting_room_' + str(meeting_rooms_id)
			meeting_room_label_name_val = request.POST[meeting_room_label_name]

			meeting_room_seats_label = 'seats_room_' + str(meeting_rooms_id)
			meeting_room_seats_label_val = request.POST[meeting_room_seats_label]

			price_room_label = 'price_room_' + str(meeting_rooms_id)
			price_room_label_val = request.POST[price_room_label]

			MeetingRoom.objects.create(
				location = new_location,
				name = meeting_room_label_name_val,
				seats = meeting_room_seats_label_val,
				price = price_room_label_val
			)

		office_rooms = request.POST.get('office_rooms', 0)

		for office_rooms_id in range(1, int(office_rooms) + 1):

			office_label_name = 'office_' + str(office_rooms_id)
			office_label_name_val = request.POST[office_label_name]

			office_seats_room_label = 'office_seats_room_' + str(office_rooms_id)
			office_seats_room_label_val = request.POST[office_seats_room_label]

			Office.objects.create(
				location = new_location,
				name = office_label_name_val,
				seats = office_seats_room_label_val
			)


		messages.success(request, 'Sede creata correttamente')

		url = reverse('crm_locations_id', kwargs = {'id': new_location.id})
		return HttpResponseRedirect(url)

class crm_locations_id(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_id, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):

		location = Location.objects.get(pk = id)
		plans = Plan.objects.filter(location = location)

		subscriptions = Subscription.objects.filter(status = "ACT", plan__location = location)

		hot_desk_active = subscriptions.filter(plan__type_of_plan = "HD").count()
		fix_desks_active = subscriptions.filter(plan__type_of_plan = "FD").count()

		private_offices_active = subscriptions.filter(plan__type_of_plan = "PO").count()
		private_offices_total = Office.objects.filter(location = location).count()

		subs_accounts = subscriptions.values_list('account', flat = True)

		accounts = Account.objects.filter(pk__in = subs_accounts)

		freelancers = accounts.filter(is_freelancer = True)
		companies = accounts.filter(is_freelancer = False)

		data = {
			"location" : location,
			"plans" : plans,
			"id" : id,
			"subscriptions" : subscriptions,
			"hot_desk_active" : hot_desk_active,
			"fix_desks_active" : fix_desks_active,
			"private_offices_active" : private_offices_active,
			"private_offices_total" : private_offices_total,
			"companies" : companies,
			"freelancers" : freelancers
		}

		template_name = "crm_locations_id.html"
		return render(request, template_name, data)

class crm_locations_id_edit(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_id_edit, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):

		location = Location.objects.get(pk = id)

		meeting_rooms = MeetingRoom.objects.filter(location = location)
		offices = Office.objects.filter(location = location)

		office_managers = Member.objects.filter(is_staff = True, is_superuser = False)
		office_managers_location = location.office_managers.all()
		office_managers = office_managers.exclude(pk__in=office_managers_location)

		data = {
			"location" : location,
			"meeting_rooms" : meeting_rooms,
			"offices" : offices,
			"office_managers" : office_managers,
			"office_managers_location" : office_managers_location
		}

		template_name = "crm_locations_id_edit.html"
		return render(request, template_name, data)

	def post(self, request, id, *args, **kwargs):

		location = Location.objects.get(pk = id)

		info_location = request.POST.get("info_location", None)
		if info_location:
			name = request.POST['name']
			address = request.POST['address']
			hot_desk = request.POST['hot_desk']
			fix_desk = request.POST['fix_desk']

			location.name = name
			location.address = address
			location.hot_desks_total = hot_desk
			location.fix_desks_total = fix_desk

			location.save()

		community_managers = request.POST.get("community_managers", None)
		if community_managers:
			location.office_managers.clear()

			cm_in_location = request.POST.getlist("cm_in_location")
			for cm in cm_in_location:
				cm_obj = Member.objects.get(pk = cm)
				location.office_managers.add(cm_obj)			

		messages.success(request, 'Dati aggiornati con successo')

		url = reverse('crm_locations_id_edit', kwargs = {'id': id})
		return HttpResponseRedirect(url)			

class crm_locations_id_edit_mr_new(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_id_edit_mr_new, self).dispatch(*args, **kwargs)

	def post(self, request, id, *args, **kwargs):
		location = Location.objects.get(pk = id)

		name = request.POST['name']
		seats = request.POST['seats']
		price = request.POST['price']

		MeetingRoom.objects.create(
			location = location,
			name = name,
			seats = seats,
			price = price
		)

		return HttpResponse()

class crm_locations_id_edit_mr_mrid(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_id_edit_mr_mrid, self).dispatch(*args, **kwargs)

	def post(self, request, id, mr_id, *args, **kwargs):

		mr_obj = get_object_or_404(MeetingRoom, pk = mr_id)

		name = request.POST['name']
		seats = request.POST['seats']
		price = request.POST['price']

		mr_obj.name = name
		mr_obj.seats = seats
		mr_obj.price = price
		mr_obj.save()

		return HttpResponse()

class crm_locations_id_edit_mr_mrid_delete(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_id_edit_mr_mrid_delete, self).dispatch(*args, **kwargs)

	def post(self, request, id, mr_id, *args, **kwargs):

		mr_obj = get_object_or_404(MeetingRoom, pk = mr_id)
		mr_obj.delete()

		return HttpResponse()

class crm_locations_id_edit_off_new(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_id_edit_off_new, self).dispatch(*args, **kwargs)

	def post(self, request, id, *args, **kwargs):
		location = Location.objects.get(pk = id)
		name = request.POST['name']
		seats = request.POST['seats']

		Office.objects.create(
			location = location,
			name = name,
			seats = seats
		)

		return HttpResponse()

class crm_locations_id_edit_off_offid(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_id_edit_off_offid, self).dispatch(*args, **kwargs)

	def post(self, request, id, off_id, *args, **kwargs):

		off_obj = get_object_or_404(Office, pk = off_id)

		name = request.POST['name']
		seats = request.POST['seats']

		off_obj.name = name
		off_obj.seats = seats
		off_obj.save()

		return HttpResponse()

class crm_locations_id_edit_off_offid_delete(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_id_edit_off_offid_delete, self).dispatch(*args, **kwargs)

	def post(self, request, id, off_id, *args, **kwargs):

		off_obj = get_object_or_404(Office, pk = off_id)

		#Check a membership exists
		exists_membership = Plan.objects.filter(office = off_obj).exists()

		if exists_membership:
			return HttpResponseBadRequest("")
		else:
			off_obj.delete()
			return HttpResponse()

class crm_locations_id_plans_new(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_id_plans_new, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):

		location = Location.objects.get(pk = id)
		plans = Plan.objects.filter(location = location)
		offices = Office.objects.filter(location = location)

		subscriptions = Subscription.objects.filter(plan__in = plans)

		data = {
			"location" : location,
			"offices" : offices,
			"plans" : plans,
			"subscriptions" : subscriptions,
		}

		template_name = "crm_locations_id_plans_new.html"
		return render(request, template_name, data)

	def post(self, request, id, *args, **kwargs):
		location = Location.objects.get(pk = id)

		name = request.POST['name']
		meeting_room_hours = request.POST.get('meeting_room_hours', None)
		if meeting_room_hours == "":
			meeting_room_hours = None

		price = request.POST['price_membership']
		type_of_plan = request.POST['type_of_membership']

		office = None
		if type_of_plan == "PO":
			office_id = request.POST['office']
			office = Office.objects.get(pk = office_id)			

		Plan.objects.create(
			name = name,
			location = location,
			price = price,
			meeting_room_hours = meeting_room_hours,
			type_of_plan = type_of_plan,
			office = office
		)

		messages.success(request, 'Piano creato con successo')

		url = reverse('crm_locations_id_plans_new', kwargs = {'id': id})
		return HttpResponseRedirect(url)	

class crm_locations_id_plans_id(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_locations_id_plans_id, self).dispatch(*args, **kwargs)

	def get(self, request, id, plan_id, *args, **kwargs):

		location = Location.objects.get(pk = id)

		plan = get_object_or_404(Plan, location = location, pk = plan_id)

		offices = Office.objects.filter(location = location)

		data = {
			"location" : location,
			"plan" : plan,
			"offices" : offices
		}

		template_name = "crm_locations_id_plans_id.html"
		return render(request, template_name, data)

	def post(self, request, id, plan_id, *args, **kwargs):

		location = Location.objects.get(pk = id)

		plan = get_object_or_404(Plan, location = location, pk = plan_id)

		offices = Office.objects.filter(location = location)

		name = request.POST['name']
		price = request.POST['price_membership']
		meeting_room_hours = request.POST['meeting_room_hours']

		type_of_plan = request.POST['type_of_membership']
		office = None
		if type_of_plan == "PO":
			office_id = request.POST['office']
			office = Office.objects.get(pk = office_id)		

		is_active = request.POST.get('is_active', False)
		if is_active:
			is_active = True

		plan.name = name
		plan.price = price
		plan.meeting_room_hours = meeting_room_hours
		plan.type_of_plan = type_of_plan
		plan.office = office
		plan.is_active = is_active
		plan.save()	


		messages.success(request, 'Piano modificato con successo')

		url = reverse('crm_locations_id_plans_id', kwargs = {'id': id, 'plan_id' : plan_id})
		return HttpResponseRedirect(url)	

class crm_accounts(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_accounts, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		user = request.user
		is_staff = user.is_staff
		is_superuser = user.is_superuser

		locations = Location.objects.all()
		accounts = Account.objects.filter()

		if is_staff and not is_superuser:
			locations = locations.filter(office_managers = user)	

		for account in accounts:
			subscriptions = Subscription.objects.filter(account = account)
			account.subscriptions = subscriptions

		data = {
			"accounts" : accounts,
			"locations" : locations
		}

		template_name = "crm_accounts.html"
		return render(request, template_name, data)

class crm_accounts_id(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_accounts_id, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):

		account = Account.objects.get(pk = id)

		subscriptions = Subscription.objects.filter(account = account)
		subs_active = subscriptions.filter(status = "ACT")

		locations_of_account = set([])
		for sub in subscriptions:
			locations_of_account.add(sub.plan.location)

		data = {
			"account" : account,
			"subscriptions" : subscriptions,
			"subs_active" : subs_active,
			"locations_of_account" : locations_of_account
		}

		template_name = "crm_accounts_id.html"
		return render(request, template_name, data)

class crm_accounts_id_plan_id(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_accounts_id_plan_id, self).dispatch(*args, **kwargs)

	def get(self, request, id, plan_id, *args, **kwargs):

		account = Account.objects.get(pk = id)
		subscription = Subscription.objects.get(pk = plan_id)

		data = {
			"account" : account,
			"subscription" : subscription
		}

		template_name = "crm_accounts_id_plan_id.html"
		return render(request, template_name, data)

	def post(self, request, id, plan_id, *args, **kwargs):

		account = Account.objects.get(pk = id)
		subscription = Subscription.objects.get(pk = plan_id)

		is_active = request.POST.get('is_active', False)
		if is_active:
			status = "ACT"
		else:
			status = "INA"

		subscription.status = status
		subscription.save()

		messages.success(request, 'Abbonamento modificato con successo')

		url = reverse('crm_accounts_id_plan_id', kwargs = {'id': id, 'plan_id' : plan_id})
		return HttpResponseRedirect(url)	

class crm_accounts_id_edit(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_accounts_id_edit, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):

		account = Account.objects.get(pk = id)

		data = {
			"account" : account
		}

		template_name = "crm_accounts_id_edit.html"
		return render(request, template_name, data)

	def post(self, request, id, *args, **kwargs):

		account = Account.objects.get(pk = id)
		
		if account.is_freelancer:
			email = request.POST['email']
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			cellphone = request.POST['cellphone']

			is_active = request.POST.get('is_active', False)
			is_active_val = "INA"
			if is_active:
				is_active = True
				is_active_val = "ACT"

			member = account.members.all().first()

			old_email = member.email
			
			email = request.POST['email']

			if email != old_email:
				email_exists = User.objects.filter(email = email).exists()
				if email_exists:
					messages.error(request, "L'email desiderata appartiene ad un Membro della piattaforma")

					url = reverse('crm_accounts_id_edit', kwargs = {'id': id})
					return HttpResponseRedirect(url)	

			member.email = email
			member.username = email
			member.first_name = first_name
			member.last_name = last_name
			member.cellphone = cellphone
			member.is_active = is_active
			member.save()

			name = first_name + " " + last_name
			account.name = name
			account.status = is_active_val
			account.save()
		else:
			name = request.POST['name']
			is_active = request.POST.get('is_active', False)
			is_active_val = "INA"
			if is_active:
				is_active = True
				is_active_val = "ACT"
			account.name = name
			account.status = is_active_val
			account.save()

		messages.success(request, 'Account modificato con successo')

		url = reverse('crm_accounts_id_edit', kwargs = {'id': id})
		return HttpResponseRedirect(url)	


class crm_accounts_id_edit_member(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_accounts_id_edit_member, self).dispatch(*args, **kwargs)

	def get(self, request, id, member_id, *args, **kwargs):

		account = Account.objects.get(pk = id)
		member = Member.objects.get(pk = member_id)

		data = {
			"account" : account,
			"member" : member
		}

		template_name = "crm_accounts_id_edit_member.html"
		return render(request, template_name, data)

	def post(self, request, id, member_id, *args, **kwargs):

		account = Account.objects.get(pk = id)
		member = Member.objects.get(pk = member_id)

		old_email = member.email
		
		email = request.POST['email']

		if email != old_email:
			email_exists = User.objects.filter(email = email).exists()
			if email_exists:
				messages.error(request, "L'email desiderata appartiene ad un Membro della piattaforma")

				url = reverse('crm_accounts_id_edit_member', kwargs = {'id': id, 'member_id' : member_id})
				return HttpResponseRedirect(url)				

		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		cellphone = request.POST['cellphone']

		is_active = request.POST.get('is_active', False)
		is_active_val = "INA"
		if is_active:
			is_active = True
			is_active_val = "ACT"

		is_primary_user = request.POST.get('is_primary_user', False)
		if is_primary_user:
			is_primary_user = True
		
		member.email = email
		member.username = email
		member.first_name = first_name
		member.last_name = last_name
		member.cellphone = cellphone
		member.is_active = is_active
		member.is_primary_user = is_primary_user
		member.save()

		messages.success(request, 'Utente modificato con successo')

		url = reverse('crm_accounts_id_edit_member', kwargs = {'id': id, 'member_id' : member_id})
		return HttpResponseRedirect(url)	


class crm_accounts_new(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_accounts_new, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):

		data = {}

		template_name = "crm_accounts_new.html"
		return render(request, template_name, data)

	def post(self, request, *args, **kwargs):
		is_freelancer = request.POST['is_freelancer']

		if is_freelancer == "false":
			is_freelancer_val = False
			name = request.POST['name']

			account_obj = Account.objects.create(
				is_freelancer = is_freelancer_val,
				name = name
			)

			url = reverse('crm_accounts_id', kwargs = {'id': account_obj.id})
			return HttpResponseRedirect(url)

		else:
			is_freelancer_val = True
			email = request.POST['email']
			check_email_existence = User.objects.filter(email = email).exists()

			if check_email_existence:
				messages.error(request, 'Email già presente nel sistema')

				url = reverse('crm_accounts_new')
				return HttpResponseRedirect(url)	
			else:
				first_name = request.POST['first_name']
				last_name = request.POST['last_name']
				cellphone = request.POST['cellphone']

				new_member = Member.objects.create_user(
					email = email,
					username = email,
					password = None,
					first_name = first_name,
					last_name = last_name,
					cellphone = cellphone,
					is_primary_user = True
				)

				name = first_name + " " + last_name

				account_obj = Account.objects.create(
					name = name,
					is_freelancer = is_freelancer_val,
				)

				account_obj.members.add(new_member)	

				url = reverse('crm_accounts_id', kwargs = {'id': account_obj.id})
				return HttpResponseRedirect(url)

class crm_accounts_id_new_plan(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_accounts_id_new_plan, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):

		account = Account.objects.get(pk = id) 

		locations = Location.objects.filter()
		for loc in locations:
			plans = Plan.objects.filter(location = loc)
			loc.plans = plans

		data = {
			"account" : account,
			"locations" : locations,
			"plans" : plans
		}

		template_name = "crm_accounts_id_new_plan.html"
		return render(request, template_name, data)

	def post(self, request, id, *args, **kwargs):

		account = Account.objects.get(pk = id) 

		plan_id = request.POST['plan_id']
		plan = Plan.objects.get(pk = plan_id)

		Subscription.objects.create(
			account = account,
			plan = plan
		)

		messages.success(request, 'Piano aggiunto con successo')

		url = reverse('crm_accounts_id', kwargs = {'id': id})
		return HttpResponseRedirect(url)			

class crm_accounts_id_new_member(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_accounts_id_new_member, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):

		account = Account.objects.get(pk = id) 

		data = {
			"account" : account
		}

		template_name = "crm_accounts_id_new_member.html"
		return render(request, template_name, data)

	def post(self, request, id, *args, **kwargs):

		account = Account.objects.get(pk = id) 

		email = request.POST['email']
		check_email_existence = User.objects.filter(email = email).exists()

		if check_email_existence:
			messages.error(request, 'Email già presente nel sistema')

			url = reverse('crm_accounts_id_new_member', kwargs = {'id': id})
			return HttpResponseRedirect(url)	

		first_name = request.POST['first_name']
		last_name = request.POST['last_name']

		cellphone = request.POST['cellphone']
		is_primary_user = request.POST.get("is_primary_user", False)

		if is_primary_user:
			primary = True
		else:
			primary = False

		new_member = Member.objects.create_user(
			email = email,
			username = email,
			password = None,
			first_name = first_name,
			last_name = last_name,
			cellphone = cellphone,
			is_primary_user = primary
		)

		account.members.add(new_member)

		messages.success(request, 'Membro aggiunto con successo')

		url = reverse('crm_accounts_id', kwargs = {'id': id})
		return HttpResponseRedirect(url)	


class crm_add_payment(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_add_payment, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):

		created_at = request.POST['created_at']

		print created_at

		try:
			created_at_obj = datetime.strptime(created_at, '%d/%m/%Y %H:%M')
		except:
			created_at = created_at.replace(" ", "")
			try:
				created_at_obj = datetime.strptime(created_at, '%d/%m/%Y')
			except:
				try:
					created_at_obj = datetime.strptime(created_at, '%d/%m/%y')
				except:
					messages.error(request, 'Pagamento non aggiunto. Il formato della data deve essere GG/MM/AAAA, ej: 31/05/2017')
					url = reverse('crm_index')
					return HttpResponseRedirect(url)

		invoice_id = request.POST['invoice_id']
		invoice_obj = Invoice.objects.get(pk = invoice_id)
		invoice_obj.date_paid = created_at_obj.date()
		invoice_obj.is_paid = True
		invoice_obj.save()

		messages.success(request, 'Pagamento aggiunto con successo')
		url = reverse('crm_index')
		return HttpResponseRedirect(url)

class crm_plans(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_plans, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		user = request.user
		is_staff = user.is_staff
		is_superuser = user.is_superuser
	
		locations = Location.objects.all()
		plans = Plan.objects.all()

		if is_staff and not is_superuser:
			locations = locations.filter(office_managers = user)
			plans = plans.filter(location__office_managers = user)

		for location in locations:
			offices = Office.objects.filter(location = location)
			location.offices = offices

		data = {
			"plans" : plans,
			"locations" : locations
		}

		template_name = "crm_plans.html"
		return render(request, template_name, data)

	def post(self, request, *args, **kwargs):

		name = request.POST['name']
		location_id = request.POST['location_id']
		price = request.POST['price_membership']
		meeting_room_hours = request.POST['meeting_room_hours']

		type_of_plan = request.POST['type_of_plan']

		office_obj = None
		if type_of_plan == "PO":
			office = request.POST.get("office", None)
			office_obj = Office.objects.get(pk = office)


		location = Location.objects.get(pk = location_id)

		Plan.objects.create(
			name = name,
			location = location,
			price = price,
			meeting_room_hours = meeting_room_hours,
			type_of_plan = type_of_plan,
			office = office_obj
		)


		messages.success(request, 'Piano creato con successo')
		url = reverse('crm_plans')
		return HttpResponseRedirect(url)

class crm_new_office_manager(View):
	@method_decorator(user_passes_test(lambda u:u.is_staff, login_url = CRM_LOGIN_URL))
	def dispatch(self, *args, **kwargs):
		return super(crm_new_office_manager, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):

		office_managers = Member.objects.filter(is_staff = True, is_superuser = False)

		data = {
			"office_managers" : office_managers
		}

		template_name = "crm_new_office_manager.html"
		return render(request, template_name, data)

	def post(self, request, *args, **kwargs):

		email = request.POST['email']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']

		check_email_existence = User.objects.filter(email = email).exists()

		if check_email_existence:
			messages.error(request, 'Email già presente nel sistema')
			url = reverse('crm_new_office_manager')
			return HttpResponseRedirect(url)

		new_cm = Member.objects.create_user(
			email = email,
			username = email,
			password = None,
			first_name = first_name,
			last_name = last_name,	
			is_staff = True		
		)

		now = str(datetime.now()) + email
		token = hashlib.sha224(now).hexdigest()

		ResetPassword.objects.create(
			user = new_cm,
			token = token
		)

		send_email_new_om(email, first_name, token)		

		messages.success(request, 'Office manager creato con successo')
		url = reverse('crm_new_office_manager')
		return HttpResponseRedirect(url)

class crm_om_setpassword(View):
	def dispatch(self, *args, **kwargs):
		return super(crm_om_setpassword, self).dispatch(*args, **kwargs)

	def get(self, request, token, *args, **kwargs):
		resetpassword_obj = get_object_or_404(ResetPassword, token = token)
		used = resetpassword_obj.used

		data = {
			"used" : used
		}

		template_name = "crm_om_setpassword.html"
		return render(request, template_name, data)

	def post(self, request, token, *args, **kwargs):
		resetpassword_obj = get_object_or_404(ResetPassword, token = token)

		password = request.POST['password']
		password2 = request.POST['password2']	
		
		len_password = len(password)

		if len_password < 8:

			data = {
				"too_short" : True
			}

			template_name = "crm_cm_setpassword.html"
			response = render(request, template_name, data)

		elif password != password2:

			data = {
				"no_match" : True
			}

			template_name = "crm_cm_setpassword.html"
			response = render(request, template_name, data)

		else:
			resetpassword_obj.used = True
			resetpassword_obj.save()

			user = resetpassword_obj.user

			user.set_password(password)
			user.save()

			response = HttpResponseRedirect(CRM_LOGIN_URL)

		return response
