from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'vehicle', 'garage', 'service', 'status', 'appointment_date', 'booked_on')
    list_filter = ('status', 'garage', 'appointment_date')
    search_fields = ('customer__email', 'vehicle__registration_number', 'garage__name')
