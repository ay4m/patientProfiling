from django.db import models
from django.core.validators import MaxValueValidator

from initializer.models import visit

class doctor_checkup(models.Model):
	visit_id = models.ForeignKey(visit, on_delete=models.CASCADE)
	prescription = models.TextField(blank=True)
	comments = models.TextField(blank=True)
	temperature = models.FloatField(null=True, blank=True, validators=[MaxValueValidator(120)])
	bp_systolic = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(999)])
	bp_diastolic = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(999)])

	#stored in centimeters
	height = models.FloatField(null=True, blank=True, validators=[MaxValueValidator(300)])

	weight = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(999)])
