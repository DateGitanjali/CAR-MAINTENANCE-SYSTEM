from django import forms
from .models import Booking
from customers.models import Vehicle
from garage.models import Garage, ServiceType

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['garage', 'vehicle', 'service', 'appointment_date', 'remarks']
        widgets = {
            'garage': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(customer=user)
