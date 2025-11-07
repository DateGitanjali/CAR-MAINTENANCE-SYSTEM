from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.RadioSelect,
        label='Select your role'
    )

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'role')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'phone', 'address')

class SelectRoleForm(forms.Form):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES,widget=forms.RadioSelect,
        label='Select your role'
    )