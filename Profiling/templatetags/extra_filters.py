from datetime import datetime

from django import template

register = template.Library()

@register.filter
def get_date(timestamp):
    timestamp = float(timestamp)
    dt = datetime.fromtimestamp(timestamp)
    return str(dt.date())
    
