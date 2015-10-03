from django.db import models
from tastypie.utils.timezone import now

class DeviceType(models.Model):
	name = models.CharField(max_length=20)

class BusType(models.Model):
	name = models.ForeignKey(DeviceType)

class MeasureType(models.Model):
	type = models.CharField(max_length=20)

class Bus(models.Model):
	name = models.CharField(max_length=20)
	type = models.ForeignKey(BusType)

class Sequence(models.Model):
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=200, blank=True)
	payload = models.CharField(max_length=100)

class Device(models.Model):
	name = models.CharField(max_length=20)
	place = models.CharField(max_length=50)
	bus = models.ManyToManyField(DeviceType, blank=True)
	sequence = models.ManyToManyField(Sequence, blank=True)

class Measure(models.Model):
	type = models.ForeignKey(MeasureType)
	device = models.ForeignKey(Device)
	value = models.FloatField()
	time = models.DateTimeField(default=now)
