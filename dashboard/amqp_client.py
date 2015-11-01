import pika

class AmqpClient():
	def __init__(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
			'amqpserver'
		))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='task', durable=True)
		self.channel.basic_qos(prefetch_count=1)

	def send(self, body):
		self.channel.basic_publish(
			exchange='',
			routing_key='task',
			body=body,
			properties=pika.BasicProperties(
				delivery_mode=2
			),
		)

		self.connection.close()

