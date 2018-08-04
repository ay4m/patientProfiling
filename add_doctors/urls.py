from django.urls import path, include

from .views import search_doctor, add_doctor

urlpatterns = [
	path('search/', search_doctor),
	path('add/', add_doctor),
]