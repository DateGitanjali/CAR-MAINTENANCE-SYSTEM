from django.contrib import admin
from .models import Garage, ServiceType, GarageService

@admin.register(Garage)
class GarageAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'approved', 'rating']

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(GarageService)
class GarageServiceAdmin(admin.ModelAdmin):
    list_display = ['garage', 'service_type', 'price', 'duration_minutes']

# Register your models here.
