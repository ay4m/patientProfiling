from django.db import models

# Create your models here.
class Account (models.Model):
    profile_name = models.CharField(max_length=200)
    user_id= models.IntegerField()
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    message=models.CharField(max_length=300)
    def __str__(self):
        return self.profile_name

class MedicalHistory (models.Model):
    profile= models.ForeignKey(Account, on_delete=models.CASCADE)
    signs = models.CharField(max_length=200)
    symptoms = models.CharField(max_length=200)
    pub_date= models.DateTimeField('date published')
    def __str__ (self):
        return self.signs

class AppointmentList (models.Model):
    profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    appointment_id = models.IntegerField()
    doctor_name = models.CharField(max_length = 200)
    appointment_time = models.DateTimeField('appointment date')

    def __str__ (self):
        return self.doctor_name

class PrescriptionsList (models.Model):
    profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    appointment = models.ForeignKey(AppointmentList, on_delete= models.CASCADE)
    medicines = models.CharField(max_length = 200)
    def __str__ (self):
        return self.appointment.doctor_name
