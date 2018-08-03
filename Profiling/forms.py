from django import forms
from accounts.models import UserAccount
from django.forms import ModelForm

class UserAccountForm(ModelForm):
    class Meta:
        model= UserAccount
        fields = ['first_name', 'middle_name', 'last_name', 'dob', 'sex', 'phone_num','email', 'qr']
