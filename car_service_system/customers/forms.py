from django import forms
from .models import CustomerProfile, Vehicle, Review


# -------------------------------------------------------
# 1️⃣ Customer Profile Form
# -------------------------------------------------------
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = [
            'phone', 'address', 'city', 'state', 'pincode',
            'date_of_birth', 'gender', 'profile_image', 'notifications_enabled'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'notifications_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'notifications_enabled': 'Enable Email & Booking Notifications',
        }


# -------------------------------------------------------
# 2️⃣ Vehicle Form
# -------------------------------------------------------
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_type', 'brand', 'model', 'year_of_manufacture',
            'fuel_type', 'registration_number', 'last_service_date'
        ]
        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_manufacture': forms.NumberInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'last_service_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


# -------------------------------------------------------
# 3️⃣ Review / Feedback Form
# -------------------------------------------------------
class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, f"{i} Stars") for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Rating'
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your feedback...'}),
        }
