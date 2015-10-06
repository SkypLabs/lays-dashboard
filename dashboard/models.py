from django.db import models
from django.contrib.auth.models import User
from tastypie.utils.timezone import now
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)

class DeviceType(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name

class BusType(models.Model):
	name = models.ForeignKey(DeviceType)

	def __str__(self):
		return self.name.name

class MeasureType(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name

class Bus(models.Model):
	name = models.CharField(max_length=20)
	type = models.ForeignKey(BusType)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Buses"

class Device(models.Model):
	name = models.CharField(max_length=20)
	place = models.CharField(max_length=50)
	type = models.ManyToManyField(DeviceType)
	bus = models.ForeignKey(Bus, blank=True, null=True)

	def __str__(self):
		return self.name

class Measure(models.Model):
	type = models.ForeignKey(MeasureType)
	device = models.ForeignKey(Device)
	value = models.FloatField()
	time = models.DateTimeField(default=now)

	def __str__(self):
		return str(self.value)

class Sequence(models.Model):
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=200, blank=True)
	payload = models.CharField(max_length=100)
	device = models.ManyToManyField(Device, blank=True)

	def __str__(self):
		return self.name
