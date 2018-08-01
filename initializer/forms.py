from django import forms

from .models import visit

class VisitForm(forms.ModelForm):
	unique_num = forms.CharField(widget = forms.HiddenInput())
	class Meta:
		model = visit
		fields = ['doctor']

class IntermediateForm(forms.Form):
	user_timestamp = forms.CharField()