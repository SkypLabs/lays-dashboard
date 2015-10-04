from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return HttpResponse("It works")

def rawdata(request):
	return HttpResponse("It works")
