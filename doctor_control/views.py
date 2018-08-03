from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import DoctorCheckupForm
from .models import doctor_checkup
from accounts.decorators import logged_in_as
from initializer.models import visit, qr_map

def add_record(request, unique_num):
	try:
		qrMapObj = qr_map.objects.get(unique_num__startswith=unique_num[:-1])
	except:
		#no record for the given unique_num
		return render(request, 'barcode_app/templates/barcode.html' , {'error': 'Invalid barcode'})

	form = DoctorCheckupForm(initial={'unique_num': unique_num})

	if request.method == 'POST':
		form = DoctorCheckupForm(request.POST)

		if form.is_valid():
			formData = form.cleaned_data
			prescription = formData['prescription']
			comments = formData['comments']


			visit_id = visit.objects.get(user_id=qrMapObj.user_id,
										 timestamp=qrMapObj.timestamp)


			doctor_checkup.objects.create(visit_id=visit_id,
										  prescription=prescription,
										  comments=comments,
										  bp_systolic=formData.get('bp_systolic', ''),
										  bp_diastolic=formData.get('bp_diastolic', ''),
										  height=formData.get('height', ''),
										  weight=formData.get('weight', ''),
										  temperature=formData.get('temperature', ''))

			return render(request, 'doctor_checkup.html', {'prescription': prescription,
															'comments': comments}
						 )

	return render(request, 'doctor_checkup.html', {'form': form})
