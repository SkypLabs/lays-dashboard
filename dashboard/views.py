from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pika
from .models import Measure, MeasureType, Device, Sequence

class AmqpClient():
	def __init__(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
			'amqpserver'
		))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='task', durable=True)

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

@login_required
def index(request):
	existing_devices = Device.objects.exists()
	existing_data = Measure.objects.exists()

	if existing_devices:
		if existing_data:
			from django.conf import settings
			settings.USE_L10N = False

			types = MeasureType.objects.values_list('name', flat=True).distinct()
			devices = Device.objects.values_list('name', flat=True).distinct()
			data = dict()

			for type in types:
				data[type] = dict()
				data[type]["devices"] = dict()
				data[type]["total"] = Measure.objects.filter(unit__type__name=type).count()

				for device in devices:
					data[type]["devices"][device] = list(reversed(Measure.objects.filter(unit__type__name=type).filter(device__name=device).order_by('-time')[:10]))

			context = {
				'existing_devices' : existing_devices,
				'existing_data' : existing_data,
				'data' : data,
			}
		else:
			context = {
				'existing_devices' : existing_devices,
				'existing_data' : existing_data,
			}
	else:
		context = {
			'existing_devices' : existing_devices,
		}

	return render(request, 'dashboard/index.html', context)

@login_required
def rawdata(request):
	existing_devices = Device.objects.exists()

	if existing_devices:
		measure = Measure.objects.order_by('time').order_by('device').reverse()

		context = {
			'existing_devices' : existing_devices,
			'measure' : measure,
		}
	else:
		context = {
			'existing_devices' : existing_devices,
		}

	return render(request, 'dashboard/rawdata.html', context)

@login_required
def rawdata_export_csv(request):
	from django.http import HttpResponse
	from django.template import loader, Context
	from datetime import datetime

	dt_format = "%Y-%m-%d_%H-%M-%S"
	dt = datetime.today()
	s = dt.strftime(dt_format)

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="lays-measures-{0}.csv"'.format(s)

	csv_data = Measure.objects.all()

	t = loader.get_template('dashboard/rawdata_export_csv.txt')
	c = Context({
		'measures': csv_data,
	})

	response.write(t.render(c))
	return response

@login_required
def send_sequence(request):
	existing_sequencies = Sequence.objects.exists()
	context = dict()

	if existing_sequencies:
		if request.GET.get('sequence_id'):
			try:
				sequence_id = request.GET['sequence_id']
				sequence = Sequence.objects.get(id=sequence_id)
				AmqpClient().send(sequence.payload)
				context['message_type'] = 'success'
				context['message_body'] = 'Sequence sent'
			except Sequence.DoesNotExist:
				context['message_type'] = 'error'
				context['message_body'] = 'The sequence does not exist'

		sequences = Sequence.objects.order_by('name')

		context['existing_sequencies'] = existing_sequencies
		context['sequencies'] = sequences
	else:
		context['existing_sequencies'] = existing_sequencies

	return render(request, 'dashboard/send_sequence.html', context)
