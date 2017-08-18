from django.conf.urls import url

from . import views

urlpatterns=[
	url(r'^$', views.index),
	url(r'^login$', views.login),  #login process
	url(r'^register$', views.register), #register process
	url(r'^travels$', views.dashboard), #show user login first page
	url(r'^logout$', views.logout),
	url(r'^enrolling/(?P<id>\d+)$', views.enrolling),
	url(r'^adding$', views.adding),  
	url(r'^travels/add$', views.add), 
	url(r'^destination/(?P<id>\d+)$', views.destination), 
	url(r'^delete/(?P<id>\d+)$', views.delete), 
]
