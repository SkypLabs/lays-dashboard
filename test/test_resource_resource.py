from django.contrib.auth.models import User, Permission
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from dashboard.models import MeasureType, MeasureUnit, Device, Resource

class ResourceResourceTest(ResourceTestCase):
	def setUp(self):
		super(ResourceResourceTest, self).setUp()

		self.username = 'user'
		self.password = 'pass'
		self.user = User.objects.create_user(self.username, 'user@example.com', self.password)

		self.device = Device.objects.create(name='stm32', place='Inside', description='STM32F4')
		self.measure_type = MeasureType.objects.create(name='Temperature')
		self.unit = MeasureUnit.objects.create(name='°C', type=self.measure_type)

		self.entry = Resource.objects.create(address=1, name="sentemp01", device=self.device, mode='ro', type='ms', dimension='vl', unit=self.unit)
		self.list_url = '/api/v1/resource/'
		self.detail_url = '/api/v1/resource/{0}/'.format(self.entry.pk)
		self.post_data = {
			'address': '2',
			'name': 'sentemp02',
			'device': '/api/v1/device/{0}/'.format(self.device.pk),
			'mode': 'ro',
			'type': 'ms',
			'dimension': 'vl',
			'unit': '/api/v1/measure_unit/{0}/'.format(self.unit.pk),
		}

	def get_credentials(self):
		return self.create_apikey(self.username, ApiKey.objects.get(user=self.user).key)

	def test_get_list_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.get(self.list_url, format='json'))

	def test_get_list_json(self):
		resp = self.api_client.get(self.list_url, format='json', authentication=self.get_credentials())

		self.assertValidJSONResponse(resp)
		self.assertEqual(len(self.deserialize(resp)['objects']), 1)
		self.assertEqual(self.deserialize(resp)['objects'][0]['address'], 1)

	def test_get_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))

	def test_get_detail_json(self):
		resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())

		self.assertValidJSONResponse(resp)
		self.assertEqual(self.deserialize(resp)['address'], 1)
		self.assertEqual(self.deserialize(resp)['name'], 'sentemp01')
		self.assertEqual(self.deserialize(resp)['device']['name'], 'stm32')
		self.assertEqual(self.deserialize(resp)['mode'], 'ro')
		self.assertEqual(self.deserialize(resp)['type'], 'ms')
		self.assertEqual(self.deserialize(resp)['dimension'], 'vl')
		self.assertEqual(self.deserialize(resp)['unit']['name'], '°C')

	def test_post_list_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json', data=self.post_data))
		self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json', data=self.post_data, authentication=self.get_credentials()))

	def test_post_list_json(self):
		self.user.user_permissions.add(Permission.objects.get(codename='add_resource'))
		self.assertEqual(Resource.objects.count(), 1)
		self.assertHttpCreated(self.api_client.post(self.list_url, format='json', data=self.post_data, authentication=self.get_credentials()))
		self.assertEqual(Resource.objects.count(), 2)

	def test_put_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))
		self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}, authentication=self.get_credentials()))

	def test_put_detail_json(self):
		self.user.user_permissions.add(Permission.objects.get(codename='change_resource'))
		self.user.user_permissions.add(Permission.objects.get(codename='change_measuretype'))
		self.user.user_permissions.add(Permission.objects.get(codename='change_measureunit'))
		self.user.user_permissions.add(Permission.objects.get(codename='change_device'))
		original_data = self.deserialize(self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials()))
		new_data = original_data.copy()
		new_data['name'] = 'sentemp03'
		new_data['address'] = '3'

		self.assertEqual(Resource.objects.count(), 1)
		self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data, authentication=self.get_credentials()))
		self.assertEqual(Resource.objects.count(), 1)

	def test_delete_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))
		self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))

	def test_delete_detail(self):
		self.user.user_permissions.add(Permission.objects.get(codename='delete_resource'))
		self.assertEqual(Resource.objects.count(), 1)
		self.assertHttpAccepted(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))
		self.assertEqual(Resource.objects.count(), 0)
