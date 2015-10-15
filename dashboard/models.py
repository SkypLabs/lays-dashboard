from django.db import models
from django.contrib.auth.models import User
from tastypie.utils.timezone import now
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)

class CommunicationType(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name

class BusType(models.Model):
	name = models.OneToOneField(CommunicationType)

	def __str__(self):
		return self.name.name

class MeasureType(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name

class MeasureUnit(models.Model):
	name = models.CharField(max_length=10, unique=True)
	type = models.ForeignKey(MeasureType)

	def __str__(self):
		return self.name + " ({0})".format(self.type.name)

class Bus(models.Model):
	name = models.CharField(max_length=20, unique=True)
	type = models.ForeignKey(BusType)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Buses"

class Device(models.Model):
	SENSOR = 'S'
	ACTUATOR = 'A'
	TYPE_CHOICES = (
		(SENSOR, 'Sensor'),
		(ACTUATOR, 'Actuator'),
	)

	name = models.CharField(max_length=20, unique=True)
	type = models.CharField(max_length=2, choices=TYPE_CHOICES)
	communication_type = models.ManyToManyField(CommunicationType)
	bus = models.ForeignKey(Bus, null=True, blank=True)
	place = models.CharField(max_length=50, null=True, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.name

class Measure(models.Model):
	unit = models.ForeignKey(MeasureUnit)
	device = models.ForeignKey(Device)
	time = models.DateTimeField(default=now)
	value = models.FloatField()

	def __str__(self):
		return str(self.value)

class Sequence(models.Model):
	name = models.CharField(max_length=20, unique=True)
	device = models.ManyToManyField(Device, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)
	payload = models.CharField(max_length=100)

	def __str__(self):
		return self.name
