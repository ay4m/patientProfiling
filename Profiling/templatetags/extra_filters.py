from datetime import datetime
from time import time

from django import template

register = template.Library()

@register.filter
def get_date(timestamp):
    timestamp = float(timestamp)
    dt = datetime.fromtimestamp(timestamp)
    dt = dt.date()
    return dt.strftime('%b %d, %Y')

@register.filter
def get_age(datestamp):
	age = datetime.date(datetime.now()) - datestamp
	return str(int(age.days / 365))
    
