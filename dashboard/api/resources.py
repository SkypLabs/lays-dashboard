from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.serializers import Serializer
from dashboard.models import MeasureType, MeasureUnit, Device, Resource, Measure

class MeasureTypeResource(ModelResource):
	class Meta:
		queryset = MeasureType.objects.all()
		resource_name = 'measure_type'
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
	class Meta:
		queryset = Device.objects.all()
		resource_name = 'device'
		ordering = ['name']
		allowed_methods = ['post', 'get', 'put', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'uuid' : ALL,
			'name' : ALL,
			'place' : ALL,
		}

class ResourceResource(ModelResource):
	device = fields.ToOneField(DeviceResource, 'device', full=True)
	unit = fields.ToOneField(MeasureUnitResource, 'unit', full=True, null=True, blank=True)

	class Meta:
		queryset = Resource.objects.all()
		resource_name = 'resource'
		ordering = ['name']
		allowed_methods = ['post', 'get', 'put', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'address' : ALL,
			'name' : ALL,
			'device' : ALL_WITH_RELATIONS,
			'mode' : ALL,
			'type' : ALL,
			'dimension' : ALL,
			'unit' : ALL_WITH_RELATIONS,
		}

class MeasureResource(ModelResource):
	unit = fields.ToOneField(MeasureUnitResource, 'unit', full=True)
	resource = fields.ToOneField(ResourceResource, 'resource', full=True)

	class Meta:
		queryset = Measure.objects.all()
		resource_name = 'measure'
		ordering = ['time']
		allowed_methods = ['post', 'get', 'put', 'delete']
		authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
		authorization = DjangoAuthorization()
		always_return_date = True
		include_resource_uri = False
		filtering = {
			'unit' : ALL_WITH_RELATIONS,
			'resource' : ALL_WITH_RELATIONS,
		}
