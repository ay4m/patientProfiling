from django import forms

from accounts.models import UserAccount, DoctorAccount, HospitalAccount, LabAccount

class LoginForm(forms.Form):
	id = forms.CharField(max_length=12, label='ID')
	password = forms.CharField(widget=forms.PasswordInput(), label='Password')

class UserRegisterForm(forms.ModelForm):
	sex = forms.ChoiceField(label='Gender*', choices=(
													('male', ('male')),
													('female', ('female')),
													('others', ('others'))),
													)
	password = forms.CharField(widget=forms.PasswordInput(), label='Password*')
	confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password*')

	def clean_phone_num(self):
		phone_num = self.cleaned_data['phone_num']

		if phone_num == '':
			return phone_num
		elif not phone_num.isdigit():
			raise forms.ValidationError('Invalid Phone Number')

		return phone_num

	def clean(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']

		if password != confirm_password:
			raise forms.ValidationError('Password and Confirm Password do not match')

	class Meta:
		model = UserAccount

		fields = ['id',
				  'first_name',
				  'middle_name',
				  'last_name',
				  'dob',
				  'sex',
				  'phone_num',
				  'email',
				  'profile_image']

		labels = {
			'id': 'ID*',
			'first_name': 'First Name*',
			'middle_name': 'Middle Name',
			'last_name': 'Last Name*',
			'dob': 'Date of Birth* (yyyy-mm-dd)',
			'phone_num': 'Phone Number',
			'email': 'E-mail Address',
			'profile_image': 'Profile Picture'
		}

class DoctorRegisterForm(UserRegisterForm):
	specialty = forms.CharField(label='Specialty*',max_length=20)
	class Meta:
		model = DoctorAccount

		fields = ['id',
				  'first_name',
				  'middle_name',
				  'last_name',
				  'dob',
				  'sex',
				  'phone_num',
				  'email',
				  'profile_image']

		labels = {
			'id': 'ID*',
			'first_name': 'First Name*',
			'middle_name': 'Middle Name',
			'last_name': 'Last Name*',
			'dob': 'Date of Birth* (yyyy-mm-dd)',
			'phone_num': 'Phone Number',
			'email': 'E-mail Address',
			'profile_image': 'Profile Picture',
		}

class LabRegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(), label='Password*')
	confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password*')
	
	def clean(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']

		if password != confirm_password:
			raise forms.ValidationError('Password and Confirm Password')

	class Meta:
		model = LabAccount

		fields = ['id',
				  'name']

		labels = {
			'id': 'ID*',
			'name': 'Lab Name*'
		}