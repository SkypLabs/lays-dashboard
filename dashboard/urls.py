from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^rawdata/$', views.rawdata, name='rawdata'),
	url(r'^rawdata/export_csv/$', views.rawdata_export_csv, name='rawdata_export_csv'),
)
