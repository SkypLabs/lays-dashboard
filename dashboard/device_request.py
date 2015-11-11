import pika
import json

class DeviceRequest():
	def __init__(self, host, uuid):
		self.host = host
		self.uuid = uuid

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
			host=self.host
		))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue=self.uuid, durable=True)
		self.channel.basic_qos(prefetch_count=1)

	def read(self, address):
		payload = {
			"address" : address,
			"action": "read",
		}
		message = json.dumps(payload)

		self.channel.basic_publish(
			exchange='',
			routing_key=self.uuid,
			body=message,
			properties=pika.BasicProperties(
				delivery_mode=2
			),
		)

		self.connection.close()

	def write(self, address, value):
		payload = {
			"address" : address,
			"action": "write",
			"value": value
		}
		message = json.dumps(payload)

		self.channel.basic_publish(
			exchange='',
			routing_key=self.uuid,
			body=message,
			properties=pika.BasicProperties(
				delivery_mode=2
			),
		)

		self.connection.close()
