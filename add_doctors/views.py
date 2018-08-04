from django.shortcuts import render

from accounts.models import DoctorAccount
from accounts.decorators import logged_in_as
from .forms import SearchForm

@logged_in_as(['Hospital'])
def search_doctor(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			search_word = form.cleaned_data['search']
			doctor_list = []

			try:
				doctor = DoctorAccount.objects.get(pk=search_word)
				doctor_list = [doctor]
			except:
				doctors = DoctorAccount.objects.extra(
						 where=["first_name || ' ' || last_name ilike %s"]
						 ,params=['%%%s%%' %search_word])
				[doctor_list.append(doctor) for doctor in doctors]

			return render(request, 'add_doctors/search.html', {'form':form,
												   'doctor_list':doctor_list})

	form = SearchForm()
	return render(request, 'add_doctors/search.html', {'form': form})

@logged_in_as(['Hospital'])
def add_doctor(request):
	if request.method=='POST':
		result = dict(request.POST)

		for key in result:
			if result[key] == ['Add Doctor']:
				doctor = DoctorAccount.objects.get(pk=key)
				request.user.doctors.add(doctor)

	form=SearchForm()
	return render(request, 'add_doctors/search.html', {'form': form})