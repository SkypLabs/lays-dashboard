from django.http import HttpResponse
from django.shortcuts import render
from .models import Measure, MeasureType, Device

def index(request):
	return HttpResponse("It works")

def rawdata(request):
	measure = Measure.objects.order_by('time').order_by('device').reverse()
	context = {
		'measure' : measure,
	}
	return render(request, 'dashboard/rawdata.html', context)
