from django.urls import path

from accounts.views import UserRegister, DoctorRegister, LabRegister, UserLogin, DoctorLogin, LabLogin, HospitalLogin, logoutView

urlpatterns = [
	path('login/user/', UserLogin.as_view()),
	path('register/user/', UserRegister.as_view()),
	path('register/doctor/', DoctorRegister.as_view()),
	path('register/lab/', LabRegister.as_view()),
	path('login/hospital/', HospitalLogin.as_view()),
	path('login/user/', UserLogin.as_view()),
	path('login/doctor/', DoctorLogin.as_view()),
	path('login/lab/', LabLogin.as_view()),
	path('logout/', logoutView),
]