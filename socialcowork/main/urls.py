from django.conf.urls import url
from django.contrib.auth.views import logout
from .views import app_index, app_login, app_bacheca_new

urlpatterns = [
	url(r'^$', app_index.as_view(), name = "app_index"),
	url(r'^logout/$', logout, {'next_page': 'app_login'}, name = "app_logout"),
	url(r'^login$', app_login.as_view(), name = "app_login"),
	url(r'^bacheca/new$', app_bacheca_new.as_view(), name = "app_bacheca_new"),

]