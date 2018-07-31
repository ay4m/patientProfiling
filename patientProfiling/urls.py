"""patientProfiling URL Configuration

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
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.core.exceptions import PermissionDenied

from accounts.views import user_type
from initializer.views import qr_mapper, set_visit
#from Profiling.views import index
from barcode_app.views import barcode_view
from doctor_control.views import add_record as doctor_addRecord

def redirect_append(request, unique_num):
	if user_type(request.user, 'Doctor'):
		return doctor_addRecord(request, unique_num)
	#elif user_type(request.user, 'Lab'):
	raise PermissionDenied

urlpatterns = [
	path('home/',TemplateView.as_view(template_name='patientProfiling/templates/index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('scan/', qr_mapper),
    path('set_visit/<slug:user_timestamp>', set_visit),
    #path('profile/<slug:user_id>', index),
    path('barcode/', barcode_view),
    path('add_record/<slug:unique_num>', redirect_append),
    path('profile/', include ('Profiling.urls')),
]
