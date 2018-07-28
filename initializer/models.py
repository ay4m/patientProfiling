from random import choice as randomChoice

from django.db import models

from accounts.models import UserAccount, DoctorAccount, HospitalAccount

class visit(models.Model):
	visit_id = models.CharField(primary_key=True, max_length=16, editable=False)
	user_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='User')
	hospital = models.ForeignKey(HospitalAccount, on_delete=models.CASCADE, related_name='Doctor')
	doctor = models.ForeignKey(DoctorAccount, on_delete=models.CASCADE)
	timestamp = models.CharField(max_length=25)
	#set as charfield as timestamp of this model
	#needs to be equal to timestamp of qr_map model

class qr_map(models.Model):
	user_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
	unique_num = models.CharField(primary_key=True , max_length=13, editable=False)
	timestamp = models.CharField(max_length=25)
