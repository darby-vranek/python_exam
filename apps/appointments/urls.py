from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^log_in/$', views.log_in, name='log_in'),
	url(r'^log_out/$', views.log_out, name='log_out'),
	url(r'^appointments/$', views.show_appointments, name='appointments'),
	url(r'^appointments/new/$', views.create_appointment, name='create_appointment'),
	url(r'^appointments/(?P<id>[0-9]+)/$', views.edit_appointment, name='edit_appointment'),
	url(r'^appointments/(?P<id>[0-9]+)/update/$', views.update_appointment, name='update_appointment'),
	url(r'^appointments/(?P<id>[0-9]+)/delete/$', views.delete_appointment, name='delete_appointment')
]
