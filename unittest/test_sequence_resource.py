from django.contrib.auth.models import User, Permission
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey
from dashboard.models import CommunicationType, BusType, Bus, Device, Sequence

class SequenceResourceTest(ResourceTestCase):
	def setUp(self):
		super(SequenceResourceTest, self).setUp()

		self.username = 'user'
		self.password = 'pass'
		self.user = User.objects.create_user(self.username, 'user@example.com', self.password)

		self.communication_type = CommunicationType.objects.create(name='I2C')
		self.bus_type = BusType.objects.create(name=self.communication_type)
		self.bus = Bus.objects.create(name='i2c01', type=self.bus_type)
		self.device = Device.objects.create(name='sentemp01', type='S', bus=self.bus, place='In the ground', description='Temperature sensor')
		self.device.communication_type.add(self.communication_type)

		self.entry = Sequence.objects.create(name='Enable sensor', description='Used to enable the sensor', payload='aabbccddeeffgg')
		self.entry.device.add(self.device)
		self.list_url = '/api/v1/sequence/'
		self.detail_url = '/api/v1/sequence/{0}/'.format(self.entry.pk)
		self.post_data = {
			'name': 'Read temperature',
			'device': [
				'/api/v1/device/{0}/'.format(self.device.pk),
			],
			'description': 'Used to read the temperature',
			'payload': 'aabbccddee',
		}

	def get_credentials(self):
		return self.create_apikey(self.username, ApiKey.objects.get(user=self.user).key)

	def test_get_list_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.get(self.list_url, format='json'))

	def test_get_list_json(self):
		resp = self.api_client.get(self.list_url, format='json', authentication=self.get_credentials())

		self.assertValidJSONResponse(resp)
		self.assertEqual(len(self.deserialize(resp)['objects']), 1)
		self.assertEqual(self.deserialize(resp)['objects'][0]['name'], 'Enable sensor')

	def test_get_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))

	def test_get_detail_json(self):
		resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())

		self.assertValidJSONResponse(resp)
		self.assertEqual(self.deserialize(resp)['name'], 'Enable sensor')
		self.assertEqual(self.deserialize(resp)['device'][0]['name'], 'sentemp01')
		self.assertEqual(self.deserialize(resp)['description'], 'Used to enable the sensor')
		self.assertEqual(self.deserialize(resp)['payload'], 'aabbccddeeffgg')

	def test_post_list_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json', data=self.post_data))
		self.assertHttpUnauthorized(self.api_client.post(self.list_url, format='json', data=self.post_data, authentication=self.get_credentials()))

	def test_post_list_json(self):
		self.user.user_permissions.add(Permission.objects.get(codename='add_sequence'))
		self.assertEqual(Sequence.objects.count(), 1)
		self.assertHttpCreated(self.api_client.post(self.list_url, format='json', data=self.post_data, authentication=self.get_credentials()))
		self.assertEqual(Sequence.objects.count(), 2)

	def test_put_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))
		self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}, authentication=self.get_credentials()))

	def test_put_detail_json(self):
		self.user.user_permissions.add(Permission.objects.get(codename='change_sequence'))
		original_data = self.deserialize(self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials()))
		new_data = original_data.copy()
		new_data['description'] = 'Used to enable the temperature sensor'

		self.assertEqual(Sequence.objects.count(), 1)
		self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data, authentification=self.get_credentials()))
		self.assertEqual(Sequence.objects.count(), 1)

	def test_delete_detail_unauthorized(self):
		self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))
		self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))

	def test_delete_detail(self):
		self.user.user_permissions.add(Permission.objects.get(codename='delete_sequence'))
		self.assertEqual(Sequence.objects.count(), 1)
		self.assertHttpAccepted(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))
		self.assertEqual(Sequence.objects.count(), 0)
