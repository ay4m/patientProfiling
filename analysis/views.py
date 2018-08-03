from django.shortcuts import render
import pickle

from accounts.models import UserAccount
from initializer.models import visit
from labpost.models import TestItem
# Create your views here.

def analyse_liver_data(request):
    def replace(given_list, old_value, new_value):
        for ind, val in enumerate(given_list):
            if val == old_value:
                given_list[ind] = new_value

        return given_list

    attr_list = ['total_bilirubin',
                 'direct_bilirubin',
                 'ALP',
                 'AST',
                 'ALT',
                 'TPC',
                 'albumin',
                 'AGR']

    attr_vals = {'total_bilirubin': None,
                 'direct_bilirubin': None,
                 'ALP': None,
                 'AST': None,
                 'ALT': None,
                 'TPC': None,
                 'albumin': None,
                 'AGR': None}

    load_model = pickle.load(open('analysis/final_model.sav','rb'))

    # test is a 1d array [age,gender,tb,db,alp,alt,ast,tp,alubumin,a/g]
    
    # here 55 is age of patient, 1 is sex 'Male' of patient, 14.1 = total bullirubin,  etc... Given in report 
    #Extract from required models
    test = []
    user = request.user
    age = user.get_age()

    if user.sex == 'male':
        sex = 1
    else:
        sex=0

    test.append(age)
    test.append(sex)

    visits = visit.objects.filter(user_id=user).order_by('-timestamp')

    print(visits)

    for visit_obj in visits:
        tests = TestItem.objects.filter(visit_id=visit_obj)

        for test_obj in tests:
            if test_obj.testName.testName in attr_list:
                if attr_vals[test_obj.testName.testName] is None:
                    attr_vals[test_obj.testName.testName] = test_obj.result

    for attr, value in attr_vals.items():
        #if not value:
         #   return render(request,{'result':'Not enough data'})        
        attr_list = replace(attr_list, attr, value)

    test = test + attr_list

    print(test)
    result = load_model.predict([test])

    print(result)
    
    # Display either Your are liver patient or you are not liver patient
    #if(result[0]==1):
     #   return render(request,{'result': 'You are at risk of a liver problem'})
   
    return render(request,'result.html',{'result':'You are not at risk of a liver problem'})