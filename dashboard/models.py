from django.db import models
from django.contrib.auth.models import User
from tastypie.utils.timezone import now
from tastypie.models import create_api_key
from haikunator import haikunate
import uuid

models.signals.post_save.connect(create_api_key, sender=User)

def get_default_device_name():
	return haikunate(tokenLength=0)

class MeasureType(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name

class MeasureUnit(models.Model):
	name = models.CharField(max_length=10, unique=True)
	type = models.ForeignKey(MeasureType)

	def __str__(self):
		return "{0} ({1})".format(self.name, self.type.name)

class Device(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	name = models.CharField(default=get_default_device_name, max_length=20, unique=True)
	place = models.CharField(max_length=50, null=True, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.name

class Resource(models.Model):
	READ_ONLY = 'ro'
	WRITE_ONLY = 'wo'
	READ_WRITE = 'rw'
	MODE_CHOICES = (
		(READ_ONLY, 'Read Only'),
		(WRITE_ONLY, 'Write Only'),
		(READ_WRITE, 'Read Write'),
	)

	MEASURE = 'ms'
	COMMAND = 'cd'
	CONFIGURATION = 'cf'
	type_dict = {
		MEASURE : 'Measure',
		COMMAND : 'Command',
		CONFIGURATION : 'Configuration',
	}
	TYPE_CHOICES = (
		(MEASURE, type_dict[MEASURE]),
		(COMMAND, type_dict[COMMAND]),
		(CONFIGURATION, type_dict[CONFIGURATION]),
	)

	BOOLEAN = 'bl'
	PERCENTAGE = 'pc'
	VALUE = 'vl'
	DIMENSION_CHOICES = (
		(BOOLEAN, 'Boolean'),
		(PERCENTAGE, 'Percentage'),
		(VALUE, 'Value'),
	)

	address = models.PositiveSmallIntegerField(unique=True)
	name = models.CharField(max_length=20, null=True, blank=True)
	device = models.ForeignKey(Device)
	mode = models.CharField(max_length=2, choices=MODE_CHOICES)
	type = models.CharField(max_length=2, choices=TYPE_CHOICES)
	dimension = models.CharField(max_length=2, choices=DIMENSION_CHOICES)
	unit = models.ForeignKey(MeasureUnit, null=True, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		if self.name:
			return "{0} @{1}".format(self.name, self.device.name)
		else:
			return "Address {0} ({1}) @{2}".format(self.address, self.type_dict[self.type], self.device.name)

class Measure(models.Model):
	unit = models.ForeignKey(MeasureUnit)
	resource = models.ForeignKey(Resource)
	time = models.DateTimeField(default=now)
	value = models.FloatField()

	def __str__(self):
		return "{0} {1}".format(str(self.value), self.unit.name)
