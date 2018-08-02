from time import time
from random import choice as randomChoice
from os import mkdir

import barcode
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

#Include model of the user account

from accounts.models import UserAccount, HospitalAccount
from accounts.decorators import logged_in_as
from .forms import VisitForm ,IntermediateForm
from .models import visit, qr_map
from patientProfiling.settings import BASE_DIR

def stringKeyGenerator(length=16, use_alpha=False):
  key_set = '0123456789'

  if use_alpha:
    key_set = '0123456789ABCDEF'

  return ''.join(randomChoice(key_set) for x in range (length))

@csrf_exempt
@logged_in_as(['Hospital'])
def qr_mapper(request):
  error=None
  if request.method == "POST":
        code = str(request.POST.get('code'))

        try:
          user = UserAccount.objects.get(qr=code)
        except:
          user = None

        print(user)
        if user:
          timestamp = str(time())

          unique_num = stringKeyGenerator(length=13)
          print(unique_num)
          #generate a unique number of length 13

          while True:
            #if record with generated unique number already exists,
            #generate another unique number.
            try:
              qr_map.objects.get(unique_num=unique_num)
              unique_num = stringKeyGenerator(length=13)
            except:
              break

          qr_map.objects.create(user_id=user,
                                unique_num=unique_num,
                                timestamp=timestamp)

          user_timestamp = str(user) + '_' + timestamp

          return render(request, 'intermediate.html', {'redirect': user_timestamp})

        else:
            error = 'User Not Found'
            return render(request, 'intermediate.html', {'redirect': 'error'})

  return render(request,'qrscan.html',{'error': error})


@logged_in_as(['Hospital'])
def set_visit(request, user_timestamp):
    if request.method =="POST" :
        form = VisitForm(request.POST)

        if form.is_valid():
            formData = form.cleaned_data

            unique_num = formData['unique_num']
            print(unique_num)
            doctor = formData['doctor']
            qrMap_obj = qr_map.objects.get(unique_num=unique_num)

            user = qrMap_obj.user_id
            timestamp = qrMap_obj.timestamp

            visit_id = stringKeyGenerator(length=16, use_alpha=True)
                
            while True:     
                try:
                  visit.objects.get(visit_id=visit_id)
                  visit_id = stringKeyGenerator(length=16, use_alpha=True)
                except:
                  break

            hospital=request.user

            visit_record = visit.objects.create(visit_id=visit_id,
                                                user_id=user,
                                                hospital=hospital,
                                                doctor=doctor,
                                                timestamp=timestamp)

            static_path = BASE_DIR + '/initializer/static/'
            save_path = static_path + str(user)
            
            try:              
              mkdir(save_path) 
            except:
              pass

            file_path = save_path + '/' + user_timestamp

            EAN = barcode.get_barcode_class('ean13')
            ean = EAN(unique_num, writer=barcode.writer.ImageWriter())

            ean.save(file_path)

            unique_num = str(user) + '/' + user_timestamp + '.png'

            return render(request, 'visit.html', {'unique_num': unique_num, 'doctor': doctor, 'user': user.get_full_name()})

    user_id, timestamp = user_timestamp.split('_')
    
    try:
      qrMap = qr_map.objects.get(user_id=user_id,
                                 timestamp__startswith=timestamp+'.')
    except:
      return render(request, 'visit.html', {'error' : 'Invalid request'})

    unique_num = qrMap.unique_num
    form = VisitForm(initial={'unique_num': unique_num})
  
    return render(request, 'visit.html', {'form': form})