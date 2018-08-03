from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404

from accounts.models import UserAccount
from doctor_control.models import doctor_checkup
#from .models import MedicalHistory, AppointmentList, PrescriptionsList
from initializer.models import visit


def index(request, user_id):
    profileobject= UserAccount.objects.get(pk=user_id)
    return render(request,'Profiling/index.html', {'profileobject': profileobject})


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
    return render(request, 'Profiling/profile-edit.html', {'form': form})

def timeline(request, user_id):
    try:
        profileobject = UserAccount.objects.get(pk=user_id)
        medicaltimeline= visit.objects.order_by('-timestamp')[:5]
    except MedicalHistory.DoesNotExist:
        raise Http404("No timeline")
    return render(request, 'Profiling/timeline.html', {'medicaltimeline': medicaltimeline, 'profileobject': profileobject})

def appointments (request, user_id):
    try:
        profileobject= UserAccount.objects.get(pk=user_id)
        appointments= visit.objects.order_by('-timestamp')[:5]
    except visit.DoesNotExist:
        raise Http404('No appointments so far')
    return render(request,'Profiling/appointments.html',{'profileobject': profileobject, 'appointments': appointments})
#
def prescriptions (request, user_id):
    try:
        profileobject= UserAccount.objects.get(pk=user_id)
        prescriptionlist = doctor_checkup.objects.order_by('-visit_id')
    except doctor_checkup.DoesNotExist:
        raise Http404("Your doctor checkup doesn't exist")
    return render(request, 'Profiling/prescriptions.html', {'profileobject': profileobject,'prescriptionlist': prescriptionlist})
#
#def labreports (request, user_id):
    #try:
    #    profileobject= Account.objects.get(pk=user_id)
#    except Account.DoesNotExist:
#        raise Http404('doesnt exist')
#    return render(request, 'Profiling/labreports.html', {'profileobject': profileobject})

# Create your views here.
