from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.template import loader, Context
from django.contrib.auth.decorators import login_required
from .models import Measure, MeasureType, Device

@login_required
def index(request):
	existing_devices = Device.objects.exists()
	existing_data = Measure.objects.exists()

	if existing_devices:
		if existing_data:
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
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="measures.csv"'

	csv_data = Measure.objects.all()

	t = loader.get_template('dashboard/rawdata_export_csv.txt')
	c = Context({
		'measures': csv_data,
	})

	response.write(t.render(c))
	return response
