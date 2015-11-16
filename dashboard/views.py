from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MeasureType, Device, Resource, Measure
from .device_request import DeviceRequest

@login_required
def index(request):
	existing_devices = Device.objects.exists()
	existing_data = Measure.objects.exists()

	if existing_devices:
		if existing_data:
			from django.conf import settings
			settings.USE_L10N = False

			types = MeasureType.objects.values_list('name', flat=True)
			devices = Device.objects.values_list('name', flat=True)
			data = dict()

			for type in types:
				data[type] = dict()
				data[type]["devices"] = dict()
				data[type]["total"] = Measure.objects.filter(unit__type__name=type).count()

				for device in devices:
					data[type]["devices"][device] = list(reversed(Measure.objects.filter(unit__type__name=type).filter(resource__device__name=device).order_by('-time')[:10]))

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
		measure = Measure.objects.order_by('time').order_by('resource__device').reverse()

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
def device_resources(request):
	from collections import OrderedDict

	existing_devices = Device.objects.exists()
	existing_resources = Resource.objects.exists()

	if existing_devices:
		if existing_resources:
			if request.GET.get('device_name'):
				try:
					device_name = request.GET['device_name']
					current_device = Device.objects.get(name=device_name).name
				except Device.DoesNotExist:
					current_device = Device.objects.order_by('name').first().name
			else:
				current_device = Device.objects.order_by('name').first().name

			if request.GET.get('tab_name'):
				current_tab = request.GET['tab_name']

				if current_tab not in ['ms', 'cd', 'cf']:
					current_tab = 'ms'
			else:
				current_tab = 'ms'

			devices = Device.objects.values_list('name', flat=True).order_by('name')
			resources = Resource.objects.filter(device__name=current_device).filter(type=current_tab)
			counters = OrderedDict()

			for device in devices:
				counters[device] = Resource.objects.filter(device__name=device).count()

			context = {
				'existing_devices' : existing_devices,
				'existing_resources' : existing_resources,
				'current_device' : current_device,
				'current_tab' : current_tab,
				'resources' : resources,
				'counters' : counters,
			}
		else:
			context = {
				'existing_devices' : existing_devices,
				'existing_resources' : existing_resources,
			}
	else:
		context = {
			'existing_devices' : existing_devices,
		}

	return render(request, 'dashboard/device_resources.html', context)

@login_required
def device_request(request):
	from django.http import JsonResponse

	data = {}
	error_code = 0

	if request.POST.get('uuid') and request.POST.get('address') and request.POST.get('action'):
		device_uuid = request.POST['uuid']
		resource_address = request.POST['address']
		action = request.POST['action']

		if action == 'read' or action == 'write':
			if Resource.objects.filter(device__uuid=device_uuid).filter(address=resource_address).count() != 0:
				from django.conf import settings
				from pika.exceptions import ConnectionClosed

				try:
					if action == 'read':
						DeviceRequest(settings.AMQP_HOST, device_uuid).read(resource_address)

						data['status'] = 'success'
						data['message'] = 'read request sent'
					else:
						if request.POST.get('value'):
							resource_value = request.POST['value']

							DeviceRequest(settings.AMQP_HOST, device_uuid).write(resource_address, resource_value)

							data['status'] = 'success'
							data['message'] = 'write request sent'
						else:
							data['status'] = 'error'
							data['message'] = 'write action requested without value'
							error_code = 400
				except ConnectionClosed:
					data['status'] = 'error'
					data['message'] = 'Unable to connect to the AMQP server'
					error_code = 500
			else:
				data['status'] = 'error'
				data['message'] = 'unknown device or resource'
				error_code = 400
		else:
			data['status'] = 'error'
			data['message'] = 'unknown action'
			error_code = 400
	else:
		data['status'] = 'error'
		data['message'] = 'bad request'
		error_code = 400

	if error_code != 0:
		response = JsonResponse(data)
		response.status_code = error_code
		return response
	else:
		return JsonResponse(data)
