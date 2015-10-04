from django.contrib import admin
from dashboard.models import DeviceType, BusType, MeasureType, Bus, Sequence, Device, Measure

admin.site.register(DeviceType)
admin.site.register(BusType)
admin.site.register(MeasureType)
admin.site.register(Bus)
admin.site.register(Sequence)
admin.site.register(Device)
admin.site.register(Measure)
