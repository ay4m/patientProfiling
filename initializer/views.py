from time import time
from random import choice as randomChoice

from django.shortcuts import render

#Include model of the user account
from accounts.models import UserAccount, HospitalAccount
from .forms import VisitForm
from .models import visit, qr_map

def stringKeyGenerator(length=16):
  return ''.join(randomChoice('0123456789ABCDEF') for x in range (length))

def qr_mapper(request):
  error=None
  if request.method == "POST":
        code = str(request.POST.get('code'))

        try:
          user = UserAccount.objects.get(qr=code)
        except:
          user = None

        if user:
            timestamp = str(time())

            unique_num = stringKeyGenerator(length=10)
            #generate a unique number of length 10

            while True:
            	#if record with generated unique number already exists,
            	#generate another unique number.
              try:
                qr_map.objects.get(unique_num=unique_num)
                unique_num = StringKeyGenerator(length=10)
              except:
                break

            qr_map.objects.create(user_id=user,
                                  unique_num=unique_num,
                                  timestamp=timestamp)

            form = VisitForm(initial={'unique_num': unique_num})

            return render(request, 'visit.html', {'form': form})

        else:
            error = 'User Not Found'
            print("Error")

  return render(request,'qrscan.html',{'error': error})

def set_visit(request, user_id):
    if request.method =="POST" :
        form = VisitForm(request.POST)

        if form.is_valid():
            formData = form.cleaned_data

            unique_num = formData['unique_num']
            doctor = formData['doctor']
            qrMap_obj = qr_map.objects.get(unique_num=unique_num)

            user = qrMap_obj.user_id
            timestamp = qrMap_obj.timestamp

            visit_id = stringKeyGenerator(length=16)
                
            while True:     
                try:
                  visit.objects.get(visit_id=visit_id)
                  visit_id = stringKeyGenerator(length=16)
                except:
                  break

            #hospital=request.user
            hospital=HospitalAccount.objects.get(id='hosp1')
            print(visit_id, user, doctor, timestamp)
            visit_record = visit.objects.create(visit_id=visit_id,
                                                user_id=user,
                                                hospital=hospital,
                                                doctor=doctor,
                                                timestamp=timestamp)

            return render(request, 'visit.html', {'unique_num':unique_num, 'doctor': doctor, 'user': user.get_full_name()})

    qrMap = qr_map.objects.filter(user_id=user_id).order_by('timestamp').reverse()[0]
    unique_num = qrMap.unique_num
    form = VisitForm(initial={'unique_num': unique_num})
    return render(request, 'visit.html', {'form': form})


