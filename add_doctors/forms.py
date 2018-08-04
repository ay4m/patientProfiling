from django import forms

from accounts.models import DoctorAccount

class SearchForm(forms.Form):
	search = forms.CharField(required=False)