from django.db import models
from django.conf import settings
from django.utils import timezone
from garage.models import Garage, ServiceType
from customers.models import Vehicle


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Service', 'In Service'),
        ('Ready', 'Ready for Pickup'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    DELIVERY_CHOICES = [
        ('Pickup', 'Pickup'),
        ('Self-Drop', 'Self-Drop'),
    ]

    booking_id = models.CharField(max_length=15, unique=True, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='bookings')
    delivery_option = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='Self-Drop')
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True, null=True)
    booked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booked_on']

    def __str__(self):
        return f"{self.booking_id} - {self.vehicle.brand} {self.vehicle.model} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.booking_id:
            timestamp = int(timezone.now().timestamp())
            self.booking_id = f"BKG{timestamp}"
        super().save(*args, **kwargs)


class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='invoice')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    generated_on = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)

    def __str__(self):
        return f"Invoice for {self.booking.booking_id}"
