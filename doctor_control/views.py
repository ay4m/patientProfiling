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
			temperature = formData['temperature']
			bp_systolic = formData['bp_systolic']
			bp_diastolic = formData['bp_diastolic']
			height = formData['height']
			weight = formData['weight']


			visit_id = visit.objects.get(user_id=qrMapObj.user_id,
										 timestamp=qrMapObj.timestamp)

			doctor_checkup.objects.create(visit_id=visit_id,
										  prescription=prescription,
										  comments=comments,
										  temperature=temperature,
										  bp_systolic= bp_systolic,
										  bp_diastolic= bp_diastolic,
										  height= height,
										  weight=weight)

			return render(request, 'doctor_checkup.html', {'prescription': prescription,
															'comments': comments,
															'profileobject': request.user
															} )

	return render(request, 'doctor_checkup.html', {'form': form,
													'profileobject': request.user,
													'unique_num': unique_num})
