from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^validate$', views.validate),
	url(r'^success$', views.success),
	url(r'^logout$', views.logout),
	url(r'^login$', views.login),
	url(r'^create', views.create),
	url(r'^show/(?P<id>\d+)$',views.show),
	url(r'^removeItem/(?P<id>\d+)',views.removeItem),
	url(r'^addItem/(?P<id>\d+)$', views.addItem)
	
]