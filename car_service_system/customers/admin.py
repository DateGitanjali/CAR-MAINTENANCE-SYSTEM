from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'registration_number', 'fuel_type', 'vehicle_type', 'customer', 'created_at')
    search_fields = ('brand', 'model', 'registration_number', 'customer__email')
    list_filter = ('fuel_type', 'vehicle_type')
