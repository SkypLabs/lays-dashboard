from datetime import datetime
from django.contrib.auth.models import User, Permission
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from dashboard.models import MeasureType, MeasureUnit, Device, Resource, Measure

class MeasureResourceTest(ResourceTestCase):
	def setUp(self):
		super(MeasureResourceTest, self).setUp()

		self.username = 'user'
		self.password = 'pass'
		self.user = User.objects.create_user(self.username, 'user@example.com', self.password)

		self.device = Device.objects.create(name='stm32', place='Inside', description='STM32F4')
		self.measure_type = MeasureType.objects.create(name='Temperature')
		self.unit = MeasureUnit.objects.create(name='°C', type=self.measure_type)
		self.resource = Resource.objects.create(address=1, name="sentemp01", device=self.device, mode='ro', type='ms', dimension='vl', unit=self.unit)

		self.entry = Measure.objects.create(unit=self.unit, resource=self.resource, time=datetime(2012, 3, 1, 13, 6, 12), value=23.3)
		self.list_url = '/api/v1/measure/'
		self.detail_url = '/api/v1/measure/{0}/'.format(self.entry.pk)
		self.post_data = {
			'unit': '/api/v1/measure_unit/{0}/'.format(self.unit.pk),
			'resource': '/api/v1/resource/{0}/'.format(self.resource.pk),
			'time': '2012-05-01T19:13:42',
			'value': '25.1',
		}

	def get_credentials(self):
		return self.create_apikey(self.username, ApiKey.objects.get(user=self.user).key)

	def test_get_list_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.get(self.list_url, format='json'))

	def test_get_list_json(self):
		resp = self.api_client.get(self.list_url, format='json', authentication=self.get_credentials())

		self.assertValidJSONResponse(resp)
		self.assertEqual(len(self.deserialize(resp)['objects']), 1)
		self.assertEqual(self.deserialize(resp)['objects'][0]['value'], 23.3)

	def test_get_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))

	def test_get_detail_json(self):
		resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())

		self.assertValidJSONResponse(resp)
		self.assertEqual(self.deserialize(resp)['unit']['name'], '°C')
		self.assertEqual(self.deserialize(resp)['resource']['name'], 'sentemp01')
		self.assertEqual(self.deserialize(resp)['time'], '2012-03-01T13:06:12')
		self.assertEqual(self.deserialize(resp)['value'], 23.3)

	def test_post_list_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json', data=self.post_data))
		self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json', data=self.post_data, authentication=self.get_credentials()))

	def test_post_list_json(self):
		self.user.user_permissions.add(Permission.objects.get(codename='add_measure'))
		self.assertEqual(Measure.objects.count(), 1)
		self.assertHttpCreated(self.api_client.post(self.list_url, format='json', data=self.post_data, authentication=self.get_credentials()))
		self.assertEqual(Measure.objects.count(), 2)

	def test_put_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))
		self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}, authentication=self.get_credentials()))

	def test_put_detail_json(self):
		self.user.user_permissions.add(Permission.objects.get(codename='change_measure'))
		self.user.user_permissions.add(Permission.objects.get(codename='change_measuretype'))
		self.user.user_permissions.add(Permission.objects.get(codename='change_measureunit'))
		self.user.user_permissions.add(Permission.objects.get(codename='change_device'))
		self.user.user_permissions.add(Permission.objects.get(codename='change_resource'))
		original_data = self.deserialize(self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials()))
		new_data = original_data.copy()
		new_data['time'] = '2012-06-01T19:15:27'
		new_data['value'] = '23.9'

		self.assertEqual(Measure.objects.count(), 1)
		self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data, authentication=self.get_credentials()))
		self.assertEqual(Measure.objects.count(), 1)

	def test_delete_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))
		self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))

	def test_delete_detail(self):
		self.user.user_permissions.add(Permission.objects.get(codename='delete_measure'))
		self.assertEqual(Measure.objects.count(), 1)
		self.assertHttpAccepted(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))
		self.assertEqual(Measure.objects.count(), 0)
