from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from tastypie.admin import ApiKeyInline
from .models import CommunicationType, BusType, MeasureType, MeasureUnit, Bus, Sequence, Device, Measure

class MeasureUnitAdmin(admin.ModelAdmin):
	list_display = ('name', 'type')

class BusAdmin(admin.ModelAdmin):
	list_display = ('name', 'type')

class SequenceAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'payload')

class DeviceAdmin(admin.ModelAdmin):
	list_display = ('name', 'place', 'bus')

class MeasureAdmin(admin.ModelAdmin):
	list_display = ('value', 'unit', 'device', 'time')

class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]

admin.site.register(CommunicationType)
admin.site.register(BusType)
admin.site.register(MeasureUnit, MeasureUnitAdmin)
admin.site.register(MeasureType)
admin.site.register(Bus, BusAdmin)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Measure, MeasureAdmin)

admin.site.unregister(User)
admin.site.register(User,UserModelAdmin)
