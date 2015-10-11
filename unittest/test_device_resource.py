from django.contrib.auth.models import User, Permission
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from dashboard.models import CommunicationType, BusType, Bus, Device

class DeviceResourceTest(ResourceTestCase):
	def setUp(self):
		super(DeviceResourceTest, self).setUp()

		self.username = 'user'
		self.password = 'pass'
		self.user = User.objects.create_user(self.username, 'user@example.com', self.password)

		self.i2c_type = CommunicationType.objects.create(name='I2C')
		self.i2c_bus_type = BusType.objects.create(name=self.i2c_type)
		self.i2c_bus = Bus.objects.create(name='i2c01', type=self.i2c_bus_type)

		self.entry = Device.objects.create(name='sentemp01', type='S', bus=self.i2c_bus, place='In the ground', description='Temperature sensor')
		self.entry.communication_type.add(self.i2c_type)
		self.list_url = '/api/v1/device/'
		self.detail_url = '/api/v1/device/{0}/'.format(self.entry.pk)
		self.post_data = {
			'name': 'sentemp02',
			'type': 'S',
			'communication_type': [
				'/api/v1/communication_type/{0}/'.format(self.i2c_type.pk),
			],
			'bus': '/api/v1/bus/{0}/'.format(self.i2c_bus.pk),
			'place': 'Outside',
			'description': 'Another temperature sensor',
		}

	def get_credentials(self):
		return self.create_apikey(self.username, ApiKey.objects.get(user=self.user).key)

	def test_get_list_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.get(self.list_url, format='json'))

	def test_get_list_json(self):
		resp = self.api_client.get(self.list_url, format='json', authentication=self.get_credentials())

		self.assertValidJSONResponse(resp)
		self.assertEqual(len(self.deserialize(resp)['objects']), 1)
		self.assertEqual(self.deserialize(resp)['objects'][0]['name'], 'sentemp01')

	def test_get_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))

	def test_get_detail_json(self):
		resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())

		self.assertValidJSONResponse(resp)
		self.assertEqual(self.deserialize(resp)['name'], 'sentemp01')
		self.assertEqual(self.deserialize(resp)['type'], 'S')
		self.assertEqual(self.deserialize(resp)['communication_type'][0]['name'], 'I2C')
		self.assertEqual(self.deserialize(resp)['bus']['name'], 'i2c01')
		self.assertEqual(self.deserialize(resp)['place'], 'In the ground')
		self.assertEqual(self.deserialize(resp)['description'], 'Temperature sensor')

	def test_post_list_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json', data=self.post_data))
		self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json', data=self.post_data, authentication=self.get_credentials()))

	def test_post_list_json(self):
		self.user.user_permissions.add(Permission.objects.get(codename='add_device'))
		self.assertEqual(Device.objects.count(), 1)
		self.assertHttpCreated(self.api_client.post(self.list_url, format='json', data=self.post_data, authentication=self.get_credentials()))
		self.assertEqual(Device.objects.count(), 2)

	def test_put_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))
		self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}, authentication=self.get_credentials()))

	def test_put_detail_json(self):
		self.user.user_permissions.add(Permission.objects.get(codename='change_device'))
		original_data = self.deserialize(self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials()))
		new_data = original_data.copy()
		new_data['name'] = 'sentemp03'
		new_data['place'] = 'Indoor'

		self.assertEqual(Device.objects.count(), 1)
		self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data, authentification=self.get_credentials()))
		self.assertEqual(Device.objects.count(), 1)

	def test_delete_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))
		self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))

	def test_delete_detail(self):
		self.user.user_permissions.add(Permission.objects.get(codename='delete_device'))
		self.assertEqual(Device.objects.count(), 1)
		self.assertHttpAccepted(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))
		self.assertEqual(Device.objects.count(), 0)
