from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from .models import MedicalHistory, AppointmentList, PrescriptionsList
from .forms import AccountForm
from accounts.models import UserAccount
def index(request, user_id):
    profileobject= UserAccount.objects.get(pk=user_id)
    return render(request,'Profiling/index.html', {'profileobject': profileobject})


def profile(request, user_id):
    # try:
    #     profileobject= UserAccount.objects.get(pk=user_id)
    # except Account.DoesNotExist:
    #     raise Http404("Profile doesn't exist")
    return render(request,'Profiling/profile.html',{'profileobject': profileobject})

def get_profile(request, user_id):
    profileobject = Account.objects.get(pk=user_id)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=profileobject)
        if form.is_valid():
            profile_ob= form.save(commit=False)
            profile_ob.save()
            return redirect('profile', user_id=profileobject.user_id)
    else:
        form = AccountForm(instance=profileobject)
    return render(request, 'Profiling/profile-edit.html', {'form': form})

def timeline(request, user_id):
    try:
        profileobject = Account.objects.get(pk=user_id)
        medicaltimeline= MedicalHistory.objects.order_by('-pub_date')[:5]
    except MedicalHistory.DoesNotExist:
        raise Http404("No timeline")
    return render(request, 'Profiling/timeline.html', {'medicaltimeline': medicaltimeline, 'profileobject': profileobject})

def appointments (request, user_id):
    try:
        profileobject= Account.objects.get(pk=user_id)
        appointments= AppointmentList.objects.order_by('-appointment_time')[:5]
    except AppointmentList.DoesNotExist:
        raise Http404('No appointments so far')
    return render(request,'Profiling/appointments.html',{'profileobject': profileobject, 'appointments': appointments})

def prescriptions (request, user_id):
    try:
        profileobject= Account.objects.get(pk=user_id)
        prescriptionlist = PrescriptionsList.objects.order_by('-appointment_time')
    except PrescriptionsList.DoesNotExist:
        raise Http404('doesnt exist')
    return render(request, 'Profiling/prescriptions.html', {'profileobject': profileobject,'prescriptionlist': prescriptionlist})

def labreports (request, user_id):
    try:
        profileobject= Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        raise Http404('doesnt exist')
    return render(request, 'Profiling/labreports.html', {'profileobject': profileobject})

# Create your views here.
