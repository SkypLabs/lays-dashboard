from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from tastypie.admin import ApiKeyInline
from .models import MeasureType, MeasureUnit, Device, Resource, Measure

class MeasureUnitAdmin(admin.ModelAdmin):
	list_display = ('name', 'type')

class DeviceAdmin(admin.ModelAdmin):
	list_display = ('uuid', 'name', 'place')

class ResourceAdmin(admin.ModelAdmin):
	list_display = ('address', 'name', 'device', 'mode', 'type', 'dimension', 'unit')

class MeasureAdmin(admin.ModelAdmin):
	list_display = ('value', 'unit', 'resource', 'time')

class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]

admin.site.register(MeasureType)
admin.site.register(MeasureUnit, MeasureUnitAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Measure, MeasureAdmin)

admin.site.unregister(User)
admin.site.register(User,UserModelAdmin)
