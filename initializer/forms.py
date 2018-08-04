from django import forms

from .models import visit

class InitialVisitForm(forms.Form):
	unique_num = forms.CharField(widget=forms.HiddenInput())

	def __init__(self, choices, *args, **kwargs):
		super(InitialVisitForm, self).__init__(*args, **kwargs)
		self.fields["specialty"] = forms.ChoiceField(choices=choices)
	

class IntermediateForm(forms.Form):
	user_timestamp = forms.CharField()

class AppointmentForm(forms.Form):
	unique_num = forms.CharField(widget=forms.HiddenInput())

	def __init__(self, choices, *args, **kwargs):
		super(AppointmentForm, self).__init__(*args, **kwargs)
		self.fields["doctor"] = forms.ChoiceField(choices=choices)