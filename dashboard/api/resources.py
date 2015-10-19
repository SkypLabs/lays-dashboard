from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from dashboard.models import CommunicationType, BusType, MeasureType, MeasureUnit, Bus, Device, Measure, Sequence
from tastypie.serializers import Serializer

class CommunicationTypeResource(ModelResource):
	class Meta:
		queryset = CommunicationType.objects.all()
		resource_name = 'communication_type'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'put', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
		}

class BusTypeResource(ModelResource):
	name = fields.ToOneField(CommunicationTypeResource, 'name', full=True)

	class Meta:
		queryset = BusType.objects.all()
		resource_name = 'bus_type'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'put', 'delete']
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
		allowed_methods = ['post', 'get', 'put', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
		}

class MeasureUnitResource(ModelResource):
	type = fields.ToOneField(MeasureTypeResource, 'type', full=True)

	class Meta:
		queryset = MeasureUnit.objects.all()
		resource_name = 'measure_unit'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'put', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
			'type' : ALL_WITH_RELATIONS,
		}

class BusResource(ModelResource):
	type = fields.ToOneField(BusTypeResource, 'type', full=True)

	class Meta:
		queryset = Bus.objects.all()
		resource_name = 'bus'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'put', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
			'type' : ALL_WITH_RELATIONS,
		}

class DeviceResource(ModelResource):
	bus = fields.ToOneField(BusResource, 'bus', full=True)
	communication_type = fields.ToManyField('dashboard.api.resources.CommunicationTypeResource', 'communication_type', full=True)

	class Meta:
		queryset = Device.objects.all()
		resource_name = 'device'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'put', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
			'type' : ALL,
			'communication_type' : ALL_WITH_RELATIONS,
			'bus' : ALL_WITH_RELATIONS,
			'place' : ALL,
		}

class MeasureResource(ModelResource):
	unit = fields.ToOneField(MeasureUnitResource, 'unit', full=True)
	device = fields.ToOneField(DeviceResource, 'device', full=True)

	class Meta:
		queryset = Measure.objects.all()
		resource_name = 'measure'
		excludes = ['id']
		ordering = ['time']
		allowed_methods = ['post', 'get', 'put', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'device' : ALL_WITH_RELATIONS,
			'unit' : ALL_WITH_RELATIONS,
		}

class SequenceResource(ModelResource):
	device = fields.ToManyField('dashboard.api.resources.DeviceResource', 'device', full=True)

	class Meta:
		queryset = Sequence.objects.all()
		resource_name = 'sequence'
		excludes = ['id']
		ordering = ['name']
		allowed_methods = ['post', 'get', 'put', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'name' : ALL,
			'device' : ALL_WITH_RELATIONS,
		}
