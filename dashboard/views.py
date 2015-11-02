from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MeasureType, Device, Measure

@login_required
def index(request):
	existing_devices = Device.objects.exists()
	existing_data = Measure.objects.exists()

	if existing_devices:
		if existing_data:
			from django.conf import settings
			settings.USE_L10N = False

			types = MeasureType.objects.values_list('name', flat=True).distinct()
			devices = Device.objects.values_list('uuid', flat=True).distinct()
			data = dict()

			for type in types:
				data[type] = dict()
				data[type]["devices"] = dict()
				data[type]["total"] = Measure.objects.filter(unit__type__name=type).count()

				for device in devices:
					data[type]["devices"][device] = list(reversed(Measure.objects.filter(unit__type__name=type).filter(resource__device__uuid=device).order_by('-time')[:10]))

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
