"""PatientProfiling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<slug:user_id>/', views.index, name='index'),
    path('<slug:user_id>/id/', views.profile, name='profile'),
    #path('<slug:user_id>/id/edit/',views.get_profile, name='get_profile'),
    path('<slug:user_id>/timeline/',views.timeline, name='timeline'),
    path('<slug:user_id>/appointments/', views.appointments, name='appointments'),
    #path('<slug:user_id>/labreports/', views.labreports, name='labreports'),
    path('<slug:user_id>/prescriptions/', views.prescriptions, name='prescriptions'),
]
