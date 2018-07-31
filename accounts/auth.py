from django.contrib.auth.backends import ModelBackend

from accounts.models import BaseAccount, HospitalAccount, UserAccount, DoctorAccount, LabAccount

class AccountsBackend(ModelBackend):
	def authenticate(self, *args, **kwargs):
		return self.downcast_user_type(super().authenticate(*args, **kwargs))

	def get_user(self, *args, **kwargs):
		return self.downcast_user_type(super().get_user(*args, **kwargs))

	def downcast_user_type(self, user):
		try:
			hospital = HospitalAccount.objects.get(pk=user.pk)
			return hospital
		except:
			pass
		try:
			doctor_user = DoctorAccount.objects.get(pk=user.pk)
			return doctor_user
		except:
			pass
		try:
			person_user = UserAccount.objects.get(pk=user.pk)
			return person_user
		except:
			pass			
		try:
			lab = LabAccount.objects.get(pk=user.pk)
			return lab
		except:
			pass

		return user
