from django import forms
from .models import *
from django.forms import ModelForm

class AccountForm(ModelForm):
    class Meta:
        model= Account
        fields = ['profile_name', 'user_id', 'email', 'password', 'phone_number', 'message']
