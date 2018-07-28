from django import forms

from .models import doctor_checkup
from initializer.models import qr_map

class DoctorCheckupForm(forms.ModelForm):
	unique_num = forms.CharField(max_length=10)

	class Meta:
		model = doctor_checkup
		fields = ['prescription', 'comments']

	def clean_unique_num(self):
		unique_num = self.cleaned_data['unique_num']
		try:
			qr_map.objects.get(unique_num=unique_num)
			return unique_num
		except:
			raise forms.ValidationError('Unique number %s does not exist'%(unique_num))
