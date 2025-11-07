from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_type',
            'brand',
            'model',
            'year_of_manufacture',
            'fuel_type',
            'registration_number',
        ]

        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter vehicle brand'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter vehicle model'}),
            'year_of_manufacture': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year of manufacture'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter registration number'}),
        }

    def clean_year_of_manufacture(self):
        year = self.cleaned_data.get('year_of_manufacture')
        if year < 1980 or year > 2050:
            raise forms.ValidationError("Please enter a valid year between 1980 and 2050.")
        return year
