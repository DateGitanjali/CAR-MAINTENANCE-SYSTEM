from django import forms
from .models import Garage, GarageService


class GarageProfileForm(forms.ModelForm):
    class Meta:
        model = Garage
        fields = ['name', 'phone', 'address', 'city', 'state', 'pincode', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class GarageServiceForm(forms.ModelForm):
    class Meta:
        model = GarageService
        fields = ['service_type', 'price', 'duration_minutes', 'custom_text']
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'custom_text': forms.TextInput(attrs={'class': 'form-control'}),
        }
