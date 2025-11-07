from django.db import models
from django.conf import settings
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

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    garage = models.ForeignKey(
        Garage,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    service = models.ForeignKey(
        ServiceType,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    booked_on = models.DateTimeField(auto_now_add=True)
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-booked_on']

    def __str__(self):
        return f"{self.vehicle} - {self.service.name} ({self.status})"
