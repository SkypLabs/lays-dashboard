from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from dashboard.models import DeviceType, BusType, MeasureType, Bus, Sequence, Device, Measure
from tastypie.serializers import Serializer

class DeviceTypeResource(ModelResource):
	class Meta:
		queryset = DeviceType.objects.all()
		resource_name = 'device_type'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'patch', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
		}

class BusTypeResource(ModelResource):
	name = fields.ForeignKey(DeviceTypeResource, 'name', full=True)

	class Meta:
		queryset = BusType.objects.all()
		resource_name = 'bus_type'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'patch', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
		}

class MeasureTypeResource(ModelResource):
	class Meta:
		queryset = MeasureType.objects.all()
		resource_name = 'measure_type'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'patch', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
		}

class BusResource(ModelResource):
	type = fields.ForeignKey(BusTypeResource, 'type', full=True)

	class Meta:
		queryset = Bus.objects.all()
		resource_name = 'bus'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'patch', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
			'type' : ALL_WITH_RELATIONS,
		}

class SequenceResource(ModelResource):
	device = fields.ToManyField('dashboard.api.resources.DeviceResource', 'device', full=True)

	class Meta:
		queryset = Sequence.objects.all()
		resource_name = 'sequence'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'patch', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
		}

class DeviceResource(ModelResource):
	bus = fields.ForeignKey(BusResource, 'bus', full=True)
	type = fields.ToManyField('dashboard.api.resources.DeviceTypeResource', 'type', full=True)

	class Meta:
		queryset = Device.objects.all()
		resource_name = 'device'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'patch', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
			'bus' : ALL_WITH_RELATIONS,
		}

class MeasureResource(ModelResource):
	type = fields.ForeignKey(MeasureTypeResource, 'type', full=True)
	device = fields.ForeignKey(DeviceResource, 'device', full=True)

	class Meta:
		queryset = Measure.objects.all()
		resource_name = 'measure'
		excludes = ['id']
		ordering = ['time']
		allowed_methods = ['post', 'get', 'patch', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'device' : ALL_WITH_RELATIONS,
			'type' : ALL_WITH_RELATIONS,
		}
