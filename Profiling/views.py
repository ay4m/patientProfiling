from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from accounts.models import UserAccount, DoctorAccount
from doctor_control.models import doctor_checkup
#from .models import MedicalHistory, AppointmentList, PrescriptionsList
from .forms import UserAccountForm
from initializer.models import visit, qr_map
import json
from accounts.decorators import logged_in_as
from labpost.views import labImageReport, labReportGenerate

@logged_in_as(['Hospital', 'Lab', 'Account'])
def entity_home(request):
    if request.user.__class__.__name__ == 'HospitalAccount':
        return render(request,'Profiling/hospital-landingpage.html')

def labLanding(request):
    return render(request, 'Profiling/lablandingpage.html')

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

def doctor_profile(request, user_id):
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
    return render(request,'Profiling/profile.html',{'profileobject': profileobject, 'user':request.user})


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
    return render(request, 'Profiling/profile-edit.html', {'form': form,
                                                           'profileobject':profileobject})

def timeline(request, user_id):
    try:
        pk=user_id
        profileobject = UserAccount.objects.get(pk=user_id)
        medicaltimeline= doctor_checkup.objects.filter(visit_id__user_id=pk)
    except:
        raise Http404('Account does not exist')

    return render(request, 'Profiling/timeline.html', {'medicaltimeline': medicaltimeline, 'profileobject': profileobject})


def appointments (request, user_id):
    try:
        pk=user_id
        profileobject= UserAccount.objects.get(pk=user_id)
        appointments= visit.objects.filter(user_id=pk)
    except visit.DoesNotExist:
        raise Http404('Account does not exist')
    return render(request,'Profiling/appointments.html',{'profileobject': profileobject, 'appointments': appointments})
#
def prescriptions (request=None, user_id=None):
    try:
        pk=user_id
        profileobject=UserAccount.objects.get(pk=user_id)
        checkup= doctor_checkup.objects.filter(visit_id__user_id=pk).order_by('-visit_id__timestamp')
    except doctor_checkup.DoesNotExist:
        raise Http404 ('No prescriptions')

    if request:    
        return render(request, 'Profiling/prescriptions.html', {'profileobject': profileobject,'prescriptionlist': checkup})
    else:
        checkup_list = []
        for item in checkup:
            checkup_list.append([item.visit_id, [item.prescription], [item.comments]])    
        return checkup_list

def patient_profile(request, unique_num):
    try:
        qrMapObj = qr_map.objects.get(unique_num__startswith=unique_num[:-1])
        profileobject = UserAccount.objects.get(id=qrMapObj.user_id)
        print(profileobject)
        return redirect('profile', user_id=profileobject)
    except:
        raise Http404('Invalid barcode')

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
def labreports (request=None, user_id=None):
    try:
       profileobject= UserAccount.objects.get(pk=user_id)
       visits = visit.objects.filter(user_id=profileobject).order_by('-timestamp')
       lab_reports = []

       for visit_obj in visits:
          test_report = labReportGenerate(visit_obj)
          img_report = labImageReport(visit_obj)
          if len(img_report) > 0 or len(test_report) > 0:
            lab_reports.append([visit_obj,test_report, img_report])

    except Account.DoesNotExist:
       raise Http404('Account does not exist')

    if request: 
        return render(request, 'Profiling/labreports.html', {'profileobject': profileobject,
                                                        'lab_reports': lab_reports})
    else:
        return lab_reports



def single_labreport(request, visit_id):
    try:
       visit_obj = visit.objects.get(pk=visit_id)
       profileobject= visit_obj.user_id
    except Account.DoesNotExist:
       raise Http404('Account does not exist')
    
    lab_reports=[]
    test_report = labReportGenerate(visit_obj)
    img_report = labImageReport(visit_obj)
    if len(img_report) > 0 or len(test_report) > 0:
        lab_reports.append([visit_obj,test_report, img_report])

    return render(request, 'Profiling/labreports.html', {'profileobject': profileobject,
                                                        'lab_reports': lab_reports})