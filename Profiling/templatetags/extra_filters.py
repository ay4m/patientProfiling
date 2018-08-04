from datetime import datetime
from time import time

from django import template

from accounts.models import HospitalAccount
from patientProfiling.settings import MEDIA_URL

register = template.Library()

@register.filter
def get_date(timestamp):
    timestamp = float(timestamp)
    dt = datetime.fromtimestamp(timestamp)
    dt = dt.date()
    return dt.strftime('%b %d, %Y')

@register.filter
def qrURL(user):
	return MEDIA_URL + 'user_' + str(user) + '/profile/qr.png'

@register.filter
def hospital_name(hospital_id):
	h = HospitalAccount.objects.get(pk=hospital_id)
	return h.name
