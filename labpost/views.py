from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import formset_factory
from django.utils import timezone

from accounts.decorators import logged_in_as
from initializer.models import qr_map, visit
from .forms import TestItemForm, TestImageForm
from .models import TestItem, TestImage

#should be logged in as Lab
@logged_in_as(['Lab'])
def add_record(request, unique_num):
    try:
        qrMapObj = qr_map.objects.get(unique_num__startswith=unique_num[:-1])
    except:
        #no record for the given unique_num
        return render(request, 'barcode_app/templates/barcode.html' , {'error': 'Invalid barcode'})

    if request.method == 'POST':
        if request.POST.get('report'):
            return HttpResponseRedirect(unique_num + '/report')
        elif request.POST.get('image'):
            return HttpResponseRedirect(unique_num + '/image')

    return render(request, 'select_record_type.html')

#should be logged in as Lab
@logged_in_as(['Lab'])
def labReportInput(request, unique_num, record_type):
    """Generate lab test input form"""
    try:
        qrMapObj = qr_map.objects.get(unique_num__startswith=unique_num[:-1])
    except:
        #no record for the given unique_num
        return render(request, 'barcode_app/templates/barcode.html' , {'error': 'Invalid barcode'})

    if record_type == 'report':
        testItemFormset = formset_factory(TestItemForm, extra=10)

        #dummy data
        #date = timezone.now().date()

        if request.method == 'POST':
            formset = testItemFormset(request.POST)
            if formset.is_valid():
                for form in formset:
                    length = len(form.cleaned_data)
                    # print("form : " + str(length))
                    # print("data : ")
                    # print(form.cleaned_data)
                    # print("form : " + str(length))
                    # print("data : ")
                    # print(form.cleaned_data)
                    if length > 0 and form.is_valid():
                        test = form.save(commit=False)
                        test.visit_id = visit.objects.get(user_id=qrMapObj.user_id,
                                                          timestamp=qrMapObj.timestamp)
                        test.lab = request.user
                        test.save()

            return HttpResponseRedirect("")

        else:
            return render(request, 'labtest.html', {'formset': testItemFormset})

    elif record_type == 'image':
        if request.method == 'POST':
            form = TestImageForm(request.POST, request.FILES)
            if form.is_valid():
                testImage = form.save(commit=False)
                testImage.visit_id = visit.objects.get(user_id=qrMapObj.user_id,
                                                       timestamp=qrMapObj.timestamp)
                testImage.lab = request.user
                testImage.save()

                return HttpResponseRedirect("")
        else:
            form = TestImageForm()

        return render(request, 'labimage.html', {'form': form, 'profileobject':request.user})

def labReportGenerate(visit_id):
    """ Generates lab report in tabular form """
    testItems = TestItem.objects.filter(visit_id=visit_id)
    
    #data to be rendered in template
    # print("name : ")
    # print(name)

    #list which contains all test records to be rendered
    testResult = []

    for test in testItems:
        #retrive information about the test record of patient
        testName = test.testName.testName
        result = test.result
        unit= test.testName.unit

        min = test.testName.minVal
        max = test.testName.maxVal
        reference = str(min) + '-' + str(max)
        
        if result >= max:
            flag = 'H'
        elif result <= min:
            flag = 'L'
        else:
            flag = '-'
        #form individual list
        testR = [testName, result, flag, unit, reference]
        #append to testResult
        testResult.append(testR)

    return testResult





#generate report of image report like Xray
def labImageReport(visit_id):
    """ Generate report of 'IMAGE FILE' uploaded to 
    patient's account """
    #dummy test data
    #SELECT * FROM TestImage WHERE user = user_id = key and dateStamp = date
    testResult = TestImage.objects.filter(visit_id=visit_id)

    return testResult
