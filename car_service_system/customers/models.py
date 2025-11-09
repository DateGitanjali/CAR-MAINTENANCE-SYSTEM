from django.db import models
from django.conf import settings
from garage.models import Garage
from bookings.models import Booking

User = settings.AUTH_USER_MODEL


# -------------------------------------------------------
# 1️⃣ Customer Profile
# -------------------------------------------------------
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    profile_image = models.ImageField(upload_to='customers/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True
    )
    notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# -------------------------------------------------------
# 2️⃣ Vehicle Information
# -------------------------------------------------------
class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('2W', 'Two Wheeler'),
        ('4W', 'Four Wheeler'),
    ]

    FUEL_TYPES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
        ('CNG', 'CNG'),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    vehicle_type = models.CharField(max_length=2, choices=VEHICLE_TYPES)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year_of_manufacture = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPES)
    registration_number = models.CharField(max_length=20, unique=True)
    last_service_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.registration_number})"


# -------------------------------------------------------
# 3️⃣ Customer Reviews / Feedback (for Garages)
# -------------------------------------------------------
class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='reviews')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'garage')  # 1 review per customer per garage
        ordering = ['-date']

    def __str__(self):
        return f"Review by {self.customer.username} for {self.garage.name} ({self.rating}⭐)"


# -------------------------------------------------------
# 4️⃣ Notifications (optional)
# -------------------------------------------------------
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"
