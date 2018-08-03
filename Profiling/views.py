from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from accounts.models import UserAccount
from doctor_control.models import doctor_checkup
#from .models import MedicalHistory, AppointmentList, PrescriptionsList
from .forms import UserAccountForm
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
#
#def labreports (request, user_id):
    #try:
    #    profileobject= Account.objects.get(pk=user_id)
#    except Account.DoesNotExist:
#        raise Http404('doesnt exist')
#    return render(request, 'Profiling/labreports.html', {'profileobject': profileobject})

# Create your views here.
