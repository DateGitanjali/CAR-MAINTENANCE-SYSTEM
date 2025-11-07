from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# -------------------------------------------------------
# Garage Profile Model
# -------------------------------------------------------
class Garage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='garage_profile')
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# -------------------------------------------------------
# Service Types (seeded list: Oil Change, Brake Repair, etc.)
# -------------------------------------------------------
class ServiceType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# -------------------------------------------------------
# Garage Services — defines what services each garage offers
# -------------------------------------------------------
class GarageService(models.Model):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='services')
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    opening_hours = models.PositiveIntegerField(default=8)
    custom_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.garage.name} - {self.service_type.name if self.service_type else 'Custom'}"


# Create your models here.
