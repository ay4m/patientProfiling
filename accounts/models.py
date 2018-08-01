from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class BaseAccountManager(BaseUserManager):
	def create_hospital(self, id, password, **kwargs):
		if not id:
			raise ValueError('id field is required')

		if not password:
			raise ValueError('password field is required')

		if not kwargs.get('name', None):
			raise ValueError('name field is required')

		if not kwargs.get('address', None):
			raise ValueError('address field is required')


		account = HospitalAccount(id=id,
								  name=kwargs.get('name', ''),
								  phone_num=kwargs.get('phone_num', ''),
								  address=kwargs.get('address'))

		account.set_password(password)
		account.save()
		return account

	def create_user(self, id, password, **kwargs):
		if not id:
			raise ValueError('id field is required')

		if not password:
			raise ValueError('password field is required')

		if not kwargs.get('first_name', None):
			raise ValueError('first_name field is required')

		if not kwargs.get('last_name', None):
			raise ValueError('last_name field is required')

		if not kwargs.get('dob', None):
			raise ValueError('dob field is required')

		if not kwargs.get('sex', None):
			raise ValueError('sex field is required')

		#if not kwargs.get('qr', None):
		#	raise ValueError('qr field is required')

		account = UserAccount(id=id,
							  first_name=kwargs.get('first_name'),
							  middle_name=kwargs.get('middle_name', ''),
							  last_name=kwargs.get('last_name'),
							  dob=kwargs.get('dob'),
							  sex=kwargs.get('sex') ,
							  phone_num=kwargs.get('phone_num', ''),
							  email=kwargs.get('email', ''),
							  qr=id
							  )

		account.set_password(password)
		account.save()
		return account

	def create_doctor(self, id, password, **kwargs):
		if not id:
			raise ValueError('id field is required')

		if not password:
			raise ValueError('password field is required')

		if not kwargs.get('first_name', None):
			raise ValueError('first_name field is required')

		if not kwargs.get('last_name', None):
			raise ValueError('last_name field is required')

		if not kwargs.get('dob', None):
			raise ValueError('dob field is required')

		if not kwargs.get('sex', None):
			raise ValueError('sex field is required')

		if not kwargs.get('specialty', None):
			raise ValueError('specialty field is required')

		account = DoctorAccount(id=id,
							  first_name=kwargs.get('first_name'),
							  middle_name=kwargs.get('middle_name', ''),
							  last_name=kwargs.get('last_name'),
							  dob=kwargs.get('dob'),
							  sex=kwargs.get('sex'),
							  phone_num=kwargs.get('phone_num', ''),
							  email=kwargs.get('email', ''),
							  specialty=kwargs.get('specialty'),
							  qr=id
							  )

		account.set_password(password)
		account.save()

		return account

	def create_lab(self, id, password, **kwargs):
		if not id:
			raise ValueError('id field is required')

		if not password:
			raise ValueError('password field is required')

		if not kwargs.get('name', None):
			raise ValueError('name field is required')

		if not kwargs.get('hospital', None):
			raise ValueError('hospital field is required')

		account = LabAccount(id=id,
							 name=kwargs.get('name'),
							 hospital=kwargs.get('hospital'))

		account.set_password(password)
		account.save()

		return account


class BaseAccount(AbstractBaseUser):
	id = models.CharField(max_length=12, primary_key=True)
	objects = BaseAccountManager()
	USERNAME_FIELD = 'id'


class HospitalAccount(BaseAccount):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=80)
	phone_num = models.CharField(max_length=15, blank=True)


class LabAccount(BaseAccount):
	name = models.CharField(max_length=100)
	hospital = models.ForeignKey('HospitalAccount', on_delete=models.CASCADE)


class UserAccount(BaseAccount):
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50)
	dob = models.DateField()
	sex = models.CharField(max_length=6)
	phone_num = models.CharField(max_length=15, blank=True)
	email = models.EmailField(max_length=80, blank=True)
	qr = models.CharField(max_length=15)

	def get_full_name(self):
		return ' '.join([self.first_name, self.middle_name, self.last_name])


class DoctorAccount(UserAccount):
	specialty = models.CharField(max_length=20)
