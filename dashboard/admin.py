from django.contrib import admin
from .models import CommunicationType, BusType, MeasureType, Bus, Sequence, Device, Measure

class BusAdmin(admin.ModelAdmin):
	list_display = ('name', 'type')

class SequenceAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'payload')

class DeviceAdmin(admin.ModelAdmin):
	list_display = ('name', 'place', 'bus')

class MeasureAdmin(admin.ModelAdmin):
	list_display = ('value', 'type', 'device', 'time')

admin.site.register(CommunicationType)
admin.site.register(BusType)
admin.site.register(MeasureType)
admin.site.register(Bus, BusAdmin)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Measure, MeasureAdmin)
