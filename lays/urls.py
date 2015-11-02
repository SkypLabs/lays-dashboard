from django.conf.urls import include, url

from tastypie.api import Api
from dashboard.api.resources import MeasureTypeResource, MeasureUnitResource, DeviceResource, ResourceResource, MeasureResource

from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(MeasureTypeResource())
v1_api.register(MeasureUnitResource())
v1_api.register(DeviceResource())
v1_api.register(ResourceResource())
v1_api.register(MeasureResource())

urlpatterns = [
	url(r'^', include('dashboard.urls', namespace="dashboard")),
	url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
