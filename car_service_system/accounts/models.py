from django.db import models
from django.contrib.auth.models import AbstractUser

# AbstractUser is a base class provided by Django for creating a custom user model. 
# It provides the full implementation of the default User model as an abstract model. This means it includes all the standard fields and methods of Django's default User model (such as username, password, email, first_name, last_name, etc.) but allows you to extend it with your own custom fields and methods. 



class UserProfile(AbstractUser):
    ROLE_CUSTOMER = 'customer'
    ROLE_GARAGE = 'garage'
    ROLE_CHOICES = [
        (ROLE_CUSTOMER, 'Customer'),
        (ROLE_GARAGE, 'Garage'),
    ]

    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_email_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.username} - {self.get_role_display()}"