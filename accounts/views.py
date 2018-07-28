from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from accounts.forms import LoginForm, UserRegisterForm
from accounts.models import UserAccount, HospitalAccount, DoctorAccount, LabAccount
from accounts.decorators import LoggedInAs

class UserRegister(View):
	template = 'register.html'

	def get(self, request):
		form = UserRegisterForm()
		return render(request, self.template, {'type': 'User', 'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)
		
		if form.is_valid():
			formData = form.cleaned_data
			UserAccount.objects.create_user(id=formData['id'],
											password=formData['password'],
											first_name=formData['first_name'],
											middle_name=formData.get('middle_name', ''),
											last_name=formData['last_name'],
											dob=formData['dob'],
											sex=formData['sex'],
											phone_num=formData.get('phone_num',''),
											email=formData.get('email', ''))
			message = """
						Thank you for registering.
						Login to use your account.
					  """
			return render(request, 'patientProfiling/templates/thankyou.html', {'message': Message})

		return render(request, self.template, {'type': 'User', 'form': form})


class DoctorRegister(View):
	template = 'register.html'

	@LoggedInAs(['Hospital'])
	def get(self, request):
	#must be logged in as Hospital
	#to register a doctor
		form = DoctorRegisterForm()
		return render(request, self.template, {'type': 'Doctor', 'form': form})

	@LoggedInAs(['Hospital'])
	def post(self, request):
		form = DoctorRegisterForm(request.POST)

		if form.is_valid():
			formData = form.cleaned_data
			UserAccount.objects.create_doctor(
											id=formData['id'],
											password=formData['password'],
											first_name=formData['first_name'],
											middle_name=formData.get('middle_name', ''),
											last_name=formData['last_name'],
											dob=formData['dob'],
											sex=formData['sex'],
											phone_num=formData.get('phone_num',''),
											email=formData.get('email', ''),
											speciality=formData['speciality']
											)

			message = """
						Thank you for registering.
						Login to use your account.
					  """
			return render(request, 'patientProfiling/templates/thankyou.html', {'message': message})

		return render(request, self.template, {'type': 'Doctor', 'form': form})


class LabRegister(View):
	template = 'register.html'

	@LoggedInAs(['Hospital'])
	def get(self, request):
	#must be logged in as Hospital
	#to register a Lab
		form = LabRegisterForm()
		return render(request, self.template, {'type': 'Lab', 'form': form})

	@LoggedInAs(['Hospital'])
	def post(self, request):
		form = LabRegisterForm(request.POST)

		if form.is_valid():
			formData = form.cleaned_data
			LabAccount.objects.create_lab(id=formData['id'],
										  password=formData['password'],
										  name=formData['name'],
										  hospital=request.user)

			message = """
						Thank you for registering.
						Login to use your account.
					  """
			return render(request, 'patientProfiling/templates/thankyou.html', {'message': message})

		return render(request, self.template, {'type': 'Lab', 'form': form})


################################## Login Views ################################ 

def user_type(user, type):
	type = type + 'Account'
	
	if user.__class__.__name__ == type:
		return True
	
	return False


class HospitalLogin(View):
	template = 'login.html'

	def get(self, request):
		form = LoginForm()
		return render(request, self.template, {'type': 'Hospital', 'form': form})

	def post(self, request):
		form = LoginForm(request.POST)

		if form.is_valid():
			formData = form.cleaned_data
			id = formData['id']
			password = formData['password']
			print(id, password)
			user = authenticate(id=id, password=password)

			if not user_type(user, 'Hospital'):
				raise PermissionDenied

			login(request, user)

			return render(request, 'patientProfiling/templates/thankyou.html', {'message': 'Login successful'})


class UserLogin(View):
	template = 'login.html'

	def get(self, request):
		form = LoginForm()
		return render(request, self.template, {'type':'User', 'form': form})

	def post(self, request):
		form = LoginForm(request.POST)
		error = None
		if form.is_valid():
			formData = form.cleaned_data
			id = formData['id']
			password = formData['password']
			print(id, password)
			user = authenticate(id=id, password=password)

			if user_type(user, 'User') or user_type(user, 'Doctor'):
				login(request, user)
				return render(request, 'patientProfiling/templates/thankyou.html', {'message': 'Login successful'})

			error = 'Invalid Credentials'

		return render(request, self.template, {'type':'User', 'form': form, 'error': error})

class DoctorLogin(View):
	template = 'login.html'

	def get(self, request):
		form = LoginForm()
		return render(request, self.template, {'type':'Doctor', 'form': form})

	def post(self, request):
		form = LoginForm(request.POST)
		error = None
		if form.is_valid():
			formData = form.cleaned_data
			id = formData['id']
			password = formData['password']
			print(id, password)
			user = authenticate(id=id, password=password)

			if user_type(user, 'Doctor'):
				login(request, user)
				return render(request, 'patientProfiling/templates/thankyou.html', {'message': 'Login successful'})

			error = 'Invalid Credentials'

		return render(request, self.template, {'type':'User', 'form': form, 'error': error})

class LabLogin(View):
	template='login.html'

	@LoggedInAs(['Hospital'])
	def get(self, request):
		form = LoginForm()
		return render(request, self.template, {'type':'Lab', 'form': form})

	@LoggedInAs(['Hospital'])
	def post(self, request):
		form = LoginForm(request.POST)
		error = None
		if form.is_valid():
			formData = form.cleaned_data
			id = formData['id']
			password = formData['password']
			
			user = authenticate(id=id, password=password)

			if user_type(user, 'Lab'):
				logout(request)
				login(request, user)
				return render(request, 'patientProfiling/templates/thankyou.html', {'message': 'Login successful'})

			raise PermissionDenied


def logoutView(request):
	logout(request)
	return HttpResponseRedirect('/home')