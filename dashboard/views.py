from django.shortcuts import render
from django.conf import settings
from .models import Measure, MeasureType, Device

def index(request):
	settings.USE_L10N = False

	types = MeasureType.objects.values_list('name', flat=True).distinct()
	devices = Device.objects.values_list('name', flat=True).distinct()
	data = dict()

	for type in types :
		data[type] = dict()
		data[type]["total_count"] = Measure.objects.filter(type__name=type).count()
		for device in devices:
			data[type][device] = Measure.objects.filter(type__name=type).filter(device__name=device).order_by('time').reverse()[:10].reverse()

	context = {
		'data' : data,
	}

	return render(request, 'dashboard/index.html', context)

def rawdata(request):
	measure = Measure.objects.order_by('time').order_by('device').reverse()

	context = {
		'measure' : measure,
	}

	return render(request, 'dashboard/rawdata.html', context)
