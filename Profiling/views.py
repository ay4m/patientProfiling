from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from accounts.models import UserAccount, DoctorAccount
from doctor_control.models import doctor_checkup
#from .models import MedicalHistory, AppointmentList, PrescriptionsList
from .forms import UserAccountForm
from initializer.models import visit
import json
from accounts.decorators import logged_in_as

@logged_in_as(['Hospital', 'Lab', 'Account'])
def entity_home(request):
    if request.user.__class__.__name__ == 'HospitalAccount':
        return render(request,'Profiling/hospital-landingpage.html')

def index(request, user_id):
    pk=user_id
    profileobject= UserAccount.objects.get(pk=user_id)
    temperatureset= doctor_checkup.objects.filter(visit_id__user_id=pk) \
        .values('visit_id','temperature')

    categories = list()
    temperature_series = list()
    bp_diastolicset= list()
    bp_systolicset = list()

    for entry in temperatureset:
        temperature_series.append(entry['temperature'])
        categories.append('Visit ID: %s' % entry['visit_id'])


    pressureset= doctor_checkup.objects.filter(visit_id__user_id=pk) \
        .values('visit_id')\
        .values('bp_diastolic','bp_systolic')\
        .order_by('visit_id')

    for entry in pressureset:
        bp_diastolicset.append(entry['bp_diastolic'])
        bp_systolicset.append(entry['bp_systolic'])

    return render(request,'Profiling/index.html', { 'bp_diastolicset': json.dumps(bp_diastolicset),
                                                    'bp_systolicset': json.dumps(bp_systolicset),
                                                    'profileobject': profileobject,
                                                    'categories': json.dumps(categories),
                                                    'temperatureset': json.dumps(temperature_series)})

def doctorviewprofile(request, user_id):
    try:
        profileobject= DoctorAccount.objects.get(pk=user_id)
    except DoctorAccount.DoesNotExist:
        raise Http404("Profile doesn't exist")
    return render(request,'Profiling/doctorprofile.html',{'profileobject': profileobject})

def profile(request, user_id):
    try:
        profileobject= UserAccount.objects.get(pk=user_id)
    except UserAccount.DoesNotExist:
        raise Http404("Profile doesn't exist")
    return render(request,'Profiling/profile.html',{'profileobject': profileobject})


def get_profile(request, user_id):
    profileobject = UserAccount.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UserAccountForm(request.POST, instance=profileobject)
        if form.is_valid():
            profileobject= form.save(commit=False)
            profileobject.save()
            return redirect('profile', user_id=profileobject.pk)
    else:
        form = UserAccountForm(instance=profileobject)
    return render(request, 'Profiling/profile-edit.html', {'form': form, 'profileobject':profileobject})

def timeline(request, user_id):
    try:
        pk=user_id
        profileobject = UserAccount.objects.get(pk=user_id)
        medicaltimeline= doctor_checkup.objects.filter(visit_id__user_id=pk)
    except doctor_checkup.DoesNotExist:
        raise Http404("No timeline")
    return render(request, 'Profiling/timeline.html', {'profileobject': profileobject,'medicaltimeline':medicaltimeline})

def appointments (request, user_id):
    try:
        pk=user_id
        profileobject= UserAccount.objects.get(pk=user_id)
        appointments= visit.objects.filter(user_id=pk)
    except visit.DoesNotExist:
        raise Http404('No appointments so far')
    return render(request,'Profiling/appointments.html',{'profileobject': profileobject, 'appointments': appointments})
#
def prescriptions (request, user_id):
    try:
        pk=user_id
        profileobject=UserAccount.objects.get(pk=user_id)
        checkup= doctor_checkup.objects.filter(visit_id__user_id=pk)
    except doctor_checkup.DoesNotExist:
        raise Http404 ('No prescriptions')
    return render(request, 'Profiling/prescriptions.html', {'profileobject': profileobject,'prescriptionlist': checkup})

def doctorappointments (request, user_id):
    try:
        pk=user_id
        profileobject= DoctorAccount.objects.get(pk=user_id)
        appointments= visit.objects.filter(doctor=user_id)
    except visit.DoesNotExist:
        raise Http404('No appointments so far')
    return render(request,'Profiling/doctorappointments.html',{'profileobject': profileobject, 'appointments': appointments})
#

#
#def labreports (request, user_id):
    #try:
    #    profileobject= Account.objects.get(pk=user_id)
#    except Account.DoesNotExist:
#        raise Http404('doesnt exist')
#    return render(request, 'Profiling/labreports.html', {'profileobject': profileobject})

# Create your views here.
