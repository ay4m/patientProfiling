from django.db import models

from initializer.models import visit

class doctor_checkup(models.Model):
	visit_id = models.ForeignKey(visit, on_delete=models.CASCADE)
	prescription = models.TextField()
	comments = models.TextField()
