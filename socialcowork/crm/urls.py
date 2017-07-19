from django.conf.urls import url
from django.contrib.auth.views import logout

from .views import crm_login
from .views import crm_locations, crm_locations_new, crm_locations_id
from .views import crm_locations_id_plans_new, crm_locations_id_plans_id
from .views import crm_locations_id_edit
from .views import crm_locations_id_edit_mr_new, crm_locations_id_edit_mr_mrid, crm_locations_id_edit_mr_mrid_delete
from .views import crm_locations_id_edit_off_new, crm_locations_id_edit_off_offid, crm_locations_id_edit_off_offid_delete
from .views import crm_accounts, crm_accounts_id, crm_accounts_new, crm_accounts_id_new_plan, crm_accounts_id_new_member
from .views import crm_accounts_id_edit
from .views import crm_add_payment
from .views import crm_accounts_id_plan_id
from .views import crm_accounts_id_edit_member
from .views import crm_payment
from .views import crm_plans
from .views import crm_new_office_manager
from .views import crm_om_setpassword

urlpatterns = [
	url(r'^$', crm_accounts.as_view(), name = "crm_index"),

	url(r'^payments$', crm_payment.as_view(), name = "crm_payment"),

	url(r'^logout/$', logout, {'next_page': 'crm_login'}, name = "crm_logout"),
	url(r'^login$', crm_login.as_view(), name = "crm_login"),

	url(r'^locations$', crm_locations.as_view(), name = "crm_locations"),
	url(r'^locations/new$', crm_locations_new.as_view(), name = "crm_locations_new"),	
	url(r'^locations/(?P<id>[0-9]+)$', crm_locations_id.as_view(), name = "crm_locations_id"),	

	url(r'^locations/(?P<id>[0-9]+)/edit$', crm_locations_id_edit.as_view(), name = "crm_locations_id_edit"),
	url(r'^locations/(?P<id>[0-9]+)/edit/mr/(?P<mr_id>[0-9]+)/$', crm_locations_id_edit_mr_mrid.as_view(), name = "crm_locations_id_edit_mr_mrid"),
	url(r'^locations/(?P<id>[0-9]+)/edit/mr/new/$', crm_locations_id_edit_mr_new.as_view(), name = "crm_locations_id_edit_mr_new"),
	url(r'^locations/(?P<id>[0-9]+)/edit/mr/(?P<mr_id>[0-9]+)/delete/$', crm_locations_id_edit_mr_mrid_delete.as_view(), name = "crm_locations_id_edit_mr_mrid_delete"),	
	url(r'^locations/(?P<id>[0-9]+)/edit/off/new/$', crm_locations_id_edit_off_new.as_view(), name = "crm_locations_id_edit_off_new"),
	url(r'^locations/(?P<id>[0-9]+)/edit/off/(?P<off_id>[0-9]+)/$', crm_locations_id_edit_off_offid.as_view(), name = "crm_locations_id_edit_off_offid"),
	url(r'^locations/(?P<id>[0-9]+)/edit/off/(?P<off_id>[0-9]+)/delete/$', crm_locations_id_edit_off_offid_delete.as_view(), name = "crm_locations_id_edit_off_offid_delete"),
	url(r'^locations/(?P<id>[0-9]+)/plans/new$', crm_locations_id_plans_new.as_view(), name = "crm_locations_id_plans_new"),
	url(r'^locations/(?P<id>[0-9]+)/plans/(?P<plan_id>[0-9]+)$', crm_locations_id_plans_id.as_view(), name = "crm_locations_id_plans_id"),

	url(r'^accounts$', crm_accounts.as_view(), name = "crm_accounts"),
	url(r'^accounts/new$', crm_accounts_new.as_view(), name = "crm_accounts_new"),
	url(r'^accounts/(?P<id>[0-9]+)$', crm_accounts_id.as_view(), name = "crm_accounts_id"),
	url(r'^accounts/(?P<id>[0-9]+)/plan/(?P<plan_id>[0-9]+)$', crm_accounts_id_plan_id.as_view(), name = "crm_accounts_id_plan_id"),
	url(r'^accounts/(?P<id>[0-9]+)/edit$', crm_accounts_id_edit.as_view(), name = "crm_accounts_id_edit"),
	url(r'^accounts/(?P<id>[0-9]+)/edit-member/(?P<member_id>[0-9]+)$', crm_accounts_id_edit_member.as_view(), name = "crm_accounts_id_edit_member"),
	url(r'^accounts/(?P<id>[0-9]+)/nuovo-piano$', crm_accounts_id_new_plan.as_view(), name = "crm_accounts_id_new_plan"),
	url(r'^accounts/(?P<id>[0-9]+)/nuovo-membro$', crm_accounts_id_new_member.as_view(), name = "crm_accounts_id_new_member"),

	url(r'^plans$', crm_plans.as_view(), name = "crm_plans"),

	url(r'^new-office-manager$', crm_new_office_manager.as_view(), name = "crm_new_office_manager"),

	url(r'^add-payment$', crm_add_payment.as_view(), name = "crm_add_payment"),

	url(r'^setpassword/(?P<token>[\w-]+)$', crm_om_setpassword.as_view(), name = "crm_om_setpassword"),	
]